# Indices for accessible web pages


from flask import render_template, flash, redirect, url_for, request
from app import app
from werkzeug.urls import url_parse
from app.forms import LoginForm, TextForm

messages = []
s = Server()
# Home Page
# Has simulation form
# Displays calculated numbers and graphs if simulation is run
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        del messages[0:]
        return redirect(url_for('chat'))
    return render_template('index.html', form=form)

# Shows the user's saved designs
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    #list = s.sentimentValue(form = TextForm())
    #list[0] = sentimentValue
    #issues = s.predict(list[1:])
    #issues is a dict with issue as key and % as val
    if form.validate_on_submit():
        analysis = s.sentimentValue(form.sms_message.data)
        issues = s.predict(analysis)
        print(analysis)
        messages.append(form.sms_message.data)

        return render_template('chat.html', form=form, messages=messages, issues=issues)
    return render_template('chat.html', form=form, messages=messages)  
