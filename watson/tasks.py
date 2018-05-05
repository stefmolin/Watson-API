# must use celery 3.1.24 on windows!
from __future__ import absolute_import, unicode_literals
from pymongo import MongoClient
from watson import utils
from watson.celery_app import celery

import logging
FORMAT = '[%(levelname)s] [ %(name)s ] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('Celery')

client = MongoClient('localhost', 27017)
db = client.data
collection = db.results

# keep the results for 24 hours only
delete_data_after_seconds = 60*60*24
collection.create_index("created_at", expireAfterSeconds=delete_data_after_seconds)

@celery.task
def simple_query(query, result_id):
    logger.debug('Querying database...')
    results = utils.query_vertica(query)
    logger.debug('Just finished querying database, results: ')
    results = utils.tag_query_results(results, result_id)
    logger.debug(results)
    logger.debug('Writing result to the database...')
    result_id = collection.insert_one(results)
    logger.debug(result_id)
    return 'Done'

@celery.task
def find_result(uuid):
    return collection.find_one({"_id" : uuid})
