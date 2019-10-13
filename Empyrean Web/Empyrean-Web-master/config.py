# Root settings for Sim Engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # Key for password reset token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key-that-is-difficult-to-guess-8684'
    
    # Initializes settings for User and Model Storage
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail for errors
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['jeremylu43@126.com']

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
