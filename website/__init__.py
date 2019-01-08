from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

from website.config import DevelopmentConfig
from os import urandom

secret_key = urandom(24)

app = Flask(__name__, static_url_path = "")

app.config.from_object('website.config.DevelopmentConfig')
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Protein_NN.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = secret_key
'''

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)

Bootstrap(app)
