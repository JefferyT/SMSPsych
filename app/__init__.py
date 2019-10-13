import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config

# Initialzies instances of flask extensions
app = Flask(__name__, static_url_path='/static')
app.static_folder = 'static'
app.config.from_object(Config)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

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
from app import routes, errors, parts
