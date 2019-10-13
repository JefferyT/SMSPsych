# Stores forms where user submits information to server

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms import DecimalField
from wtforms.validators import DataRequired, ValidationError
from app.parts import part_dict

# Takes all neccessary fields to run simulations and create graphs
# for power loss, efficiency, and compensation
class LoginForm(FlaskForm):
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Enter')

class TextForm(FlaskForm):
    sms_message = StringField('', validators=[DataRequired()])
    submit = SubmitField('Send')
