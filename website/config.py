import os
from datetime import timedelta
from base64 import b64encode

secret_key = os.urandom(24)
jwt_secret_key = b64encode('I_love_my_smokes!')

class BaseConfig(object):

    SECRET_KEY = secret_key

    SQLALCHEMY_DATABASE_URI = 'sqlite:///Protein_NN.db'
    SQLALCHEMY_TRACK_MODIFICATION = False

    #WT_SECRET_KEY = jwt_secret_key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_TOKEN_LOCATION = 'cookies'
    #JWT_ACCESS_COOKIE_PATH = '/NN/'
    #JWT_REFRESH_COOKIE_PATH ='/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False

    SESSION_COOKIE_SECURE = True

    PROPAGATE_EXCEPTIONS = True




class DevelopmentConfig(BaseConfig):

    DEBUG = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=5)

    SESSION_COOKIE_SECURE = False


    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_PORT = 587  # This is for TLS
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    #MAIL_USERNAME = os.environ['EMAIL_USER']
    #MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    #BOOTSTRAP_SERVE_LOCAL = True



