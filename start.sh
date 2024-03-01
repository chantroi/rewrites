#!/usr/bin/bash

#python -m gunicorn --reload -b 0.0.0.0:10808 wsgi:app
python -m hypercorn main:app --bind '0.0.0.0:10808' --reload