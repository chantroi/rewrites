#!/usr/bin/bash

#python -m gunicorn -w 4 -t 4 -b 0.0.0.0:10808 wsgi:app
python -m uvicorn main:app --host 0.0.0.0 --port 10808 --reload