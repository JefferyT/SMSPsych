# Classes which are stored in database

import jwt
from app import app, db, login
from time import time
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

# User Class
# Contain id, unique username, unique email, password hash, and designs
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    designs = db.relationship('Design', backref='author', lazy='dynamic')

    # prints username
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Takes in a password and generates unique hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks that the unhashed password hash matche the inputted password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Gets token for password reset, which expires in 10 minutes
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # If token matches, allows user to reset password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

# Circuit(?) Design Class
# Contain id, parameters, time of creation/edit, user it belongs to
class Design(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #parameters for circuit
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Loads a user and corresponding database
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


