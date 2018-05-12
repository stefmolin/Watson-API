#!/bin/sh
celery -A watson worker --loglevel=debug -Ofair
