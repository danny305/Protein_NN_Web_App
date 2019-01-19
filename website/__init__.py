from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from mailjet_rest import Client

from config import DevelopmentConfig, ProductionConfig
from os import environ,getcwd

pwd = getcwd()
app = Flask(__name__, static_url_path = "")
env_config = environ['APP_CONFIG']

#environ['PATH'] += ':' + pwd
print(pwd)
config_object = 'website.config.{}'.format(env_config)
app.config.from_object(config_object)
#app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
mj = Client(auth=(app.config['MJ_API_PUBLIC_KEY'],
                  app.config['MJ_API_PRIVATE_KEY']))
bs = Bootstrap(app)



from . import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)