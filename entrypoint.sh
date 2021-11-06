#!/bin/bash

if [ -z "$1"]
    then
        echo "No arguments supplied"
        exit 1
elif [ "$1" = "migrate" ]
    then
       exec export FLASK_APP=src && flask db upgrade
elif [ "$1" = "run" ]
    then
        exec gunicorn --bind=0.0.0.0:5000 \
                      --access-logfile - \
                      --error-logfile - \
                      --log-level info \
                      --workers 3 \
                      src.wsgi:app
        exit $?
else
    echo "invalid paramm"
    exit 1
fi