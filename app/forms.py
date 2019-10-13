# Stores forms where user submits information to server

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms import DecimalField
from wtforms.validators import DataRequired, ValidationError
from app.parts import part_dict

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

class LoginForm(FlaskForm):
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Enter')
