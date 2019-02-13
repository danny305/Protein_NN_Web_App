#!/bin/bash

#source ./flask_env.sh -P
source ./flask_env.sh -D

# nohup gunicorn --bind 0.0.0.0:8000 --log-level=debug wsgi:app &
# nohup gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app &
gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app

#This command will only work on a linux server and is not for running within a docker container.np
# sudo systemctl start nginx