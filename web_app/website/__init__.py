from flask import Flask
#from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from mailjet_rest import Client

from .config import DevelopmentConfig, ProductionConfig
from os import environ,getcwd

import logging

pwd = getcwd()
app = Flask(__name__, static_url_path = "")
env_config = environ.get('APP_CONFIG',"ProductionConfig")

#environ['PATH'] += ':' + pwd
print(pwd)
config_object = 'website.config.{}'.format(env_config)
app.config.from_object(config_object)
#app.config.from_pyfile('config.py')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    #logging.basicConfig()     #Uncomment this line to successfully perform a db migration.
    app.logger.setLevel(gunicorn_logger.level)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
#csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
mj = Client(auth=(app.config['MJ_API_PUBLIC_KEY'],
                  app.config['MJ_API_PRIVATE_KEY']))
bs = Bootstrap(app)



from . import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)