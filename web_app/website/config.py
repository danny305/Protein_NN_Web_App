import os
from datetime import timedelta
from base64 import b64encode

secret_key = os.urandom(24)
mail_secret_key = os.urandom(24)
mail_salt = os.urandom(24)
jwt_secret_key = b64encode('I_love_my_smokes!')

class BaseConfig(object):

    # FLASK SETTINGS
    SECRET_KEY = os.environ.get('SECRET_KEY', secret_key)
    PROPAGATE_EXCEPTIONS = True
    #SESSION_COOKIE_SECURE = True #ONLY set to True if HTTPS is enabled.
    #SERVER_NAME = '52.12.118.101:8000'


    # DATABASE SETTINGS
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Protein_NN.db'
    SQLALCHEMY_TRACK_MODIFICATION = False


    # JWT SETTINGS
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', jwt_secret_key)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False

    #JWT_ACCESS_COOKIE_PATH = '/NN/'
    #JWT_REFRESH_COOKIE_PATH ='/token/refresh'


    # EMAIL SETTINGS
    MAIL_SECRET_KEY = os.environ.get('MAIL_SECRET_KEY', mail_secret_key)
    MAIL_SALT = mail_salt
    MAIL_SERVER = os.environ.get("MAIL_SERVER", 'smtp.mail.yahoo.com')

    MAIL_PORT = os.environ.get("MAIL_PORT", 587)  # SSL 465 (google) TLS 587 (yahoo)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)

    MAIL_USERNAME = os.environ['MAIL_USER']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = os.environ['MAIL_USER']


    # MAILJET SETTINGS
    MJ_API_PUBLIC_KEY = os.environ.get('MJ_API_PUBLIC_KEY', None)
    MJ_API_PRIVATE_KEY = os.environ.get('MJ_API_PRIVATE_KEY', None)
    MJ_SERVER = "in-v3.mailjet.com"
    MJ_PORT = 587 #This port does not work for TLS use 465 instead




    #BOOTSTRAP SETTINGS
    #BOOTSTRAP_SERVE_LOCAL = True




class DevelopmentConfig(BaseConfig):

    DEBUG = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)


class ProductionConfig(BaseConfig):

    DEBUG =False





