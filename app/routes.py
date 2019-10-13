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
        return redirect(url_for('chat'))
    return render_template('index.html', form=form)

# Shows the user's saved designs
@app.route('/chat')
def chat():
    return render_template('chat.html')  
