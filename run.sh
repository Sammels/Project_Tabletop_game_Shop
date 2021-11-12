#!/bin/bash
python createadmin.py $VAR1 $VAR2
export FLASK_APP=src && export FLASK_ENV=development && flask run --host=0.0.0.0
