from os import walk
from os.path import join
import uuid
import datetime
import decimal
import yaml
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

CONF = yaml.load(open('config.yml'))
user = CONF['database']['user']
key = open(CONF['database']['key_path'], 'rb').read()
f = Fernet(key)
token = CONF['database']['token']
password = f.decrypt(token).decode('utf8')
uri = CONF['database']['uri']
db_uri = uri.format(user=user, password=password)

def generate_uuid(elements):
    unique_id = uuid.UUID('00000000-0000-0000-0000-000000000000')
    for element in elements:
        unique_id = uuid.uuid5(unique_id, str(element))
    return unique_id.hex

def tag_query_results(results, result_id):
    return {'_id' : result_id, 'created_at' : datetime.datetime.now(), 'results' : results}

def read_query_from_file(filename):
    with open(filename, 'r') as file:
        sql_query = file.read()
    return sql_query

def retrieve_query(api_resource):
    return 'queries' + api_resource.split('query', maxsplit=1)[1] + '.sql'

def get_query_files(dir):
    file_paths = []
    level = 0
    for dirpath, dirnames, filenames in walk(dir):
        if level == 0:
            file_paths.extend([file for file in filenames if '.sql' in file])
        else:
             file_paths.extend([join(dirpath.split(dir + '/')[1], file) for file in filenames if '.sql' in file])
        level += 1
    return file_paths

def query_vertica(query, db_uri=db_uri):
    engine = create_engine(db_uri, echo=False)
    try:
        results = engine.execute(query).fetchall()
        results = [dict(row) for row in results]
        # convert dates to datetime to avoid MongoDB error from dates without times; also handle Decimal
        for row in results:
            for key, value in row.items():
                if isinstance(value, datetime.date):
                    # row[key] = datetime.datetime.combine(value, datetime.time.min)
                    row[key] = str(value)
                if isinstance(value, decimal.Decimal):
                    row[key] = float(value)
    except ProgrammingError as e:
        results = {'error' : e.orig.__str__(),
                   'message' : 'The query you provided is invalid. Try running it against the database yourself to see the error.'}
    finally:
        engine.dispose
    return results
