import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
#from flask_excel import Excel

# Initialzies instances of flask extensions
app = Flask(__name__, static_url_path='/static')
app.static_folder = 'static'
app.config.from_object(Config)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)
migrate = Migrate(app, db) # migrates
login = LoginManager(app) # handles logins for users
login.init_app(app)
login.login_view = 'login' 
mail = Mail(app)
#excel.init_app(excel)

#@login.user_loader
#def load_user(user_id):
#    return None

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/simulator.log', maxBytes=10240,
                                        backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname):s%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Simulation startup')


# Imports urls, classes, errors
from app import routes, models, errors, parts
