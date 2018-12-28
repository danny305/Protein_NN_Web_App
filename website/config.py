import os
secret_key = os.urandom(24)



class Config(object):

    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Protein_NN.db'
    SQLALCHEMY_TRACK_MODIFICATION = False




