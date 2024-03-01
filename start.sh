#!/usr/bin/bash

#python -m gunicorn --reload -b 0.0.0.0:10808 wsgi:app
python -m hypercorn main:app --host 0.0.0.0 --port 10808 --reload