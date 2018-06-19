#!/bin/sh
uwsgi --http 0.0.0.0:80 -t 15 --manage-script-name --module api --callable app
