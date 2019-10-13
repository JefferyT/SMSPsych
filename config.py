# Root settings for Sim Engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # Key for password reset token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key-that-is-difficult-to-guess-8684'
