# Stores forms where user submits information to server

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms import DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from app.parts import part_dict

# Creates form for Login
# Asks for username, password, if user wants to be rememberd, and a submit button
# username and password must contain content
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Creates form for Registration
# Asks for username, email, password, password confirmation, and submit button
# username, email, password fields must be filled
# password and password confirmation must be the same
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # checks that username is not already being used
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # checks that email address is not already being used
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Takes all neccessary fields to run simulations and create graphs
# for power loss, efficiency, and compensation
class SimulationForm(FlaskForm):
    part_number = SelectField('Part Number', choices=part_dict, validators=[DataRequired()])
    switching_frequency = DecimalField('Switching Frequency', validators=[DataRequired()])
    input_voltage = DecimalField('Input Voltage (3.8V - 32V)', validators=[DataRequired()])
    output_voltage = DecimalField('Output Voltage', validators=[DataRequired()])
    output_current = DecimalField('Output Current', validators=[DataRequired()])
    ripple_ratio = DecimalField(
        'Inductor Current Ripple Ratio (\u0394I/ILOAD)', validators=[DataRequired()])
    output_inductor = DecimalField('Output Inductor (Isat > 5.5A)', validators=[DataRequired()])
    dcr = DecimalField('DCR', validators=[DataRequired()])
    num_capacitors = DecimalField(
        'Number of Output Capcitators', validators=[DataRequired()])
    capacitance_each = DecimalField(
        'Capacitance (Each)', validators=[DataRequired()])
    esr_each = DecimalField('ESR (Each)', validators=[DataRequired()])
    v_on = DecimalField('V_on', validators=[DataRequired()])
    v_off = DecimalField('V_off', validators=[DataRequired()])
    thermal_resistance = DecimalField(
        'Thermal Resistance, \u03B8ja', validators=[DataRequired()])
    ambient_temperature = DecimalField(
        'Ambient Temperature T\u209A', validators=[DataRequired()])
    min_current = DecimalField('Min Current', validators=[DataRequired()])
    max_current = DecimalField('Max Current', validators=[DataRequired()])
    user_selects_R2 = DecimalField('User Selects R2', validators=[DataRequired()])
    user_selects_C4 = DecimalField('User Selects C4', validators=[DataRequired()])
    R5_selected = DecimalField('R5 Selected Values', validators=[DataRequired()])
    C5_selected = DecimalField('C5 Selected Values', validators=[DataRequired()])
    C6_selected = DecimalField('C6 Selected Values', validators=[DataRequired()])
    submit = SubmitField('Calculate')

# Asks for email to send password reset link to
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

# Asks for password and password confirmation
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
