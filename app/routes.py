# Indices for accessible web pages

from flask import render_template, flash, redirect, url_for, request
from app import app
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.engines import *

# Home Page
# Has simulation form
# Displays calculated numbers and graphs if simulation is run
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('chat.html')
    return render_template('index.html', form=form)

# Shows the user's saved designs
@app.route('/designs')
def designs():
    return render_template('designs.html', title='My Designs') 
                         
# Displays power loss graph
@app.route('/_power_loss.html')
def _power_loss():
    return render_template('_power_loss.html')

# Displays efficiency summary graph
@app.route('/_efficiency_summary.html')
def _efficiency_summary():
    return render_template('_efficiency_summary.html')

# Displays compensation graphs
@app.route('/_compensation.html')
def _compensation():
    return render_template('_compensation.html')
