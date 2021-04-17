#!/bin/sh
python manage.py collectstatic --noinput
pkill gunicorn
gunicorn --bind 127.0.0.1:8000 amazon_web.wsgi -D