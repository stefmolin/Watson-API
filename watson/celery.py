from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

rabbit_mq_user = os.environ['RABBITMQ_USER']
rabbit_mq_pass = os.environ['RABBITMQ_PASS']

celery = Celery('watson',
                broker='pyamqp://{username}:{password}@rabbitmq.watson_api//'\
                        .format(username=rabbit_mq_user, password=rabbit_mq_pass),
                backend="rpc://",
                include=['watson.tasks'])

celery.conf.update(broker_heartbeat = 60,
                   broker_transport_options = {'confirm_publish': True})

if __name__ == '__main__':
    celery.start()
