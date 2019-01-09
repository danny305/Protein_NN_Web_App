import os
from datetime import timedelta

secret_key = os.urandom(24)
jwt_secret = os.urandom(24)

class BaseConfig(object):

    SECRET_KEY = secret_key

    SQLALCHEMY_DATABASE_URI = 'sqlite:///Protein_NN.db'
    SQLALCHEMY_TRACK_MODIFICATION = False

    JWT_SECRET_KEY = jwt_secret
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_REFRESH_COOKIE_PATH ='/token/refresh'

    SESSION_COOKIE_SECURE = True




class DevelopmentConfig(BaseConfig):

    DEBUG = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=20)

    SESSION_COOKIE_SECURE = False

    #PROPOGATE_EXCEPTION = True

    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_PORT = 587  # This is for TLS
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    #MAIL_USERNAME = os.environ['EMAIL_USER']
    #MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    #BOOTSTRAP_SERVE_LOCAL = True



