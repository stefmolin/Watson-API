from os import walk
from os.path import join
import uuid
import datetime
import decimal
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

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
            # note that for linux '\\' will need to be changed to '/'
            file_paths.extend([join(dirpath.split(dir + '\\')[1], file).replace('\\', '/') for file in filenames if '.sql' in file])
        level += 1
    return file_paths

def query_vertica(query):
    with open('secrets/cred.txt', 'r') as file:
        password = file.read().split("\n")[0]
    db_uri = 'vertica+vertica_python://{username}:{password}@<hostname>:<port>/<db>?ConnectionLoadBalance=true'\
             .format(username='s.molin', password=password)
    engine = create_engine(db_uri, echo=False)
    try:
        results = engine.execute(query).fetchall()
        results = [dict(row) for row in results]
    except ProgrammingError as e:
        results = {'error' : e.orig.__str__(),
                   'message' : 'The query you provided is invalid. Try running it against the database yourself to see the error.'}
    finally:
        engine.dispose
    return results

# this may not be necessary
def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
