from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
import yaml

rabbit_mq = yaml.load(open('config.yml'))['message_queue']
rabbit_mq_user = os.environ['RABBITMQ_USER']
rabbit_mq_pass = os.environ['RABBITMQ_PASS']

celery = Celery('watson',
                broker='pyamqp://{username}:{password}@{mq}//?heartbeat=30'\
                        .format(username=rabbit_mq_user,
                                password=rabbit_mq_pass,
                                mq=rabbit_mq),
                backend="rpc://",
                include=['watson.tasks'],
                transport_options = {'confirm_publish': True})

celery.conf.update(transport_options = {'confirm_publish': True})

if __name__ == '__main__':
    celery.start()
