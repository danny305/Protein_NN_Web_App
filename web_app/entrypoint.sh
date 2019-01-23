#!/bin/bash

source ./flask_env.sh -P

#gunicorn --bind 0.0.0.0:8000 --log-level=debug wsgi:app
gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app
