#!/bin/bash

source ./flask_env.sh -P

#gunicorn --bind 0.0.0.0:8000 --log-level=debug wsgi:app
gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app

#This command will only work on a linux server and is not for running within a docker container.np
# sudo systemctl start nginx