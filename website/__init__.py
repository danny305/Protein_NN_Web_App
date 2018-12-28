from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from website.config import Config
from os import urandom

secret_key = urandom(24)

app = Flask(__name__, static_url_path = "")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Protein_NN.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = secret_key


db = SQLAlchemy(app)
migrate = Migrate(app=app,db=db)
mail = Mail(app)
Bootstrap(app)
