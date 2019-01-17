from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from mailjet_rest import Client

from website.config import DevelopmentConfig, ProductionConfig
from os import environ


app = Flask(__name__, static_url_path = "")
env_config = environ['APP_CONFIG']
config_object = 'website.config.{}'.format(env_config)
app.config.from_object(config_object)
#app.config.from_object('website.config.ProductionConfig')


db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
mj = Client(auth=(app.config['MJ_API_PUBLIC_KEY'],app.config['MJ_API_PRIVATE_KEY']))
bs = Bootstrap(app)
