#!/bin/bash

if  [[ -z "$1" ]]; then
        echo "No arguments supplied"
        exit 1
elif [[ "$1" = "migrate" ]]; then
       exec export FLASK_APP=src && flask db upgrade

elif [[ "$1" = "run" ]]; then
        python createadmin.py $VAR1 $VAR2
        exec gunicorn --bind=0.0.0.0:$PORT \
                      --access-logfile - \
                      --error-logfile - \
                      --log-level info \
                      --workers 1 \
                      src.wsgi:app
        exit $?
else
    echo "invalid paramm"
    exit 1
fi
