import os
secret_key = os.urandom(24)



class DevelopmentConfig(object):

    DEBUG = True
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Protein_NN.db'
    SQLALCHEMY_TRACK_MODIFICATION = False

    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_PORT = 587  # This is for TLS
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    #MAIL_USERNAME = os.environ['EMAIL_USER']
    #MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    #BOOTSTRAP_SERVE_LOCAL = True



