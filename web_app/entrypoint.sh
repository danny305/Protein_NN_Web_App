#!/bin/bash

#source ./flask_env.sh -P
source ./flask_env.sh -P

#make sure you check which ip and port nginx is forwarding all traffic to.
	# This is when you are running gunicorn without nginx
# nohup gunicorn --bind 0.0.0.0:8000 --log-level=debug wsgi:app &
	# This is when nginx is is forwarding traffic to localhost.
nohup gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app &
	#This is when you are testing gunicorn in development on you localhost
# gunicorn --bind 127.0.0.1:8000 --log-level=debug wsgi:app

#This command will only work on a linux server and is not for running within a docker container.np
sudo systemctl start nginx
echo 'Starting Nginx as a proxy server.'
