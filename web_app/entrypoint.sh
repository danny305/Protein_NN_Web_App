#!/bin/bash

source ./flask_env.sh -P
gunicorn --bind localhost wsgi:app
