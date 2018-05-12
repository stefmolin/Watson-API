from flask import Flask, jsonify, request, Response, Blueprint, url_for
from flask_api import status
from celery.result import AsyncResult
from watson.celery import celery
from watson import tasks, utils
import logging
import os
import random
import re
import os

# Logging configuration
FORMAT = '[%(levelname)s] [ %(name)s ] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(os.path.basename(__file__))

api_version = 'v1'
api = Blueprint(api_version, __name__)

app = Flask(__name__)

def run_query_in_background():
    logger.debug('Generating unique ID for request...')
    sql_query_file = utils.retrieve_query(request.path)
    query_parameters = {}
    if request.args:
        # the query has parameters that need to be replaced
        id_elements = [request.args.get(key) for key in sorted(request.args.keys())]

        # make sure that integers will work with the queries
        for key, value in request.args.items():
            # try to prevent SQL injection
            try:
                value = value[:value.index(';')]
            except ValueError:
                pass
            if re.search('\\d+', value):
                try:
                    query_parameters[key] = int(value)
                except ValueError:
                    query_parameters[key] = value
            else:
                query_parameters[key] = value
    else:
        # the query will run without filling in parameters so ID will just be the query name (added later)
        id_elements = []
    id_elements.append(sql_query_file)
    result_id = utils.generate_uuid(id_elements)

    logger.debug('Locating the query...')
    sql_query = utils.read_query_from_file(sql_query_file)
    current_task = None
    if not tasks.find_result(result_id):
        # this has not already been queried for so return the url
        try:
            sql_query = re.sub('[\[\]]', '', sql_query.format(**query_parameters))
            logger.debug('Successfully replaced parameters in query.')
        except KeyError:
            logger.info('User attempting to query resource without required parameters; terminating request.')
            return api_response({'error' : 'query_error',
                                'query' : sql_query,
                                'required_parameters' : [re.sub('[\{\}]', '', missing_arg)
                                                        for missing_arg in re.findall('\\{.*?\\}', sql_query)],
                                'provided_parameters' : request.args,
                                'message' : 'Not all required parameters for the query were provided in the request.'},
                                status.HTTP_400_BAD_REQUEST)
        logger.info("Running query with celery, since we don't have the result already")
        current_task = tasks.simple_query.delay(query=sql_query, result_id=result_id)
    return api_response({'request' : sql_query,
                        'result': url_for('v1.get_results', result_id=result_id, _external=True),
                        'current_status' : current_task.status if current_task else 'none',
                        'task_id' : current_task.task_id if current_task else 'none',
                        'check_status' : url_for('v1.check_status', task_id=current_task.task_id, _external=True) if current_task else 'none'},
                        status.HTTP_202_ACCEPTED)

# create endpoints for all the queries
for query in utils.get_query_files('queries'):
    logger.debug('Creating endpoint: ' + '/query/' + query.replace('.sql', ''))
    api.add_url_rule('/query/' + query.replace('.sql', ''),
                     view_func=run_query_in_background,
                     methods=['POST'])

@api.route('/get_results/<result_id>', methods=['GET'])
def get_results(result_id): # this will be the only endpoint for geting the results
    logger.info("Getting query results")
    result = tasks.find_result(result_id)
    if result:
        # data is ready, return it
        return api_response(result, status.HTTP_200_OK)
    else:
        return api_response({'results' : 'pending'}, status.HTTP_204_NO_CONTENT)

@api.route('/check_status/<task_id>', methods=['GET'])
def check_status(task_id):
    logger.info("Checking the status of task.")
    task = AsyncResult(task_id, app=celery)
    if task:
        # task found return status
        return api_response({'task_id' : task_id,
                            'current_status' : task.status,
                            'successful' : task.successful()}, status.HTTP_200_OK)
    else:
        return api_response({'task_id' : task_id,
                            'current_status' : 'No such task exists',
                            'successful' : False}, status.HTTP_200_OK)

# this must come after defining the blueprint entirely
app.register_blueprint(api, url_prefix='/api/' + api_version)

def api_response(data, error_code=None, cache=False):
    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    if error_code:
        response.status_code = error_code
    if cache:
        response.cache_control.max_age = 86400
    return response

@app.errorhandler(404)
def page_not_found(e):
    data = {'error': 'not_found',
            'message': "No resource seems to match this endpoint URL."}
    return api_response(data, error_code=404)

@app.errorhandler(500)
def internal_server_error(e):
    data = {'error': 'unexpected_server_error',
            'message': "Oops. Something went very wrong."}
    return api_response(data, error_code=500)

@app.route('/healthcheck')
def healthcheck():
    return '', status.HTTP_200_OK

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
