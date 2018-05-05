from __future__ import absolute_import, unicode_literals
from celery import Celery

celery = Celery('watson',
                broker='amqp://guest@localhost//',
                backend="rpc://",
                include=['watson.tasks'])

if __name__ == '__main__':
    celery.start()
