#!/bin/bash
# python -m unittest discover
# coverage run -m unittest discover -s tests/
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
uwsgi --socket 0.0.0.0:${SERVICE_PORT} --protocol=http -w wsgi