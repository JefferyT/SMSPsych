# Indices for accessible web pages

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User, Design
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, SimulationForm
from app.forms import ResetPasswordForm, ResetPasswordRequestForm
from flask_login import current_user, login_user, login_required, logout_user
from app.email_user import send_password_reset_email
from app.engines import *

# Home Page
# Has simulation form
# Displays calculated numbers and graphs if simulation is run
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SimulationForm()
    if form.validate_on_submit():
        #try:
        output = AP64350.sim(form.data)
        flash('Simulation Ran!')
        return render_template('index.html', form=form, simulated=True, simmed=output)
        #except
        # flash('Calculation Error, Try again.')
    return render_template('index.html', form=form, simulated=False)

# Login Page
# Redirects to index page if user is already logged in
# If user tried to access login protected site, will redirect to previous site
# Has redirect to Register for new users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Registers a new user
# Redirects to index page if user is already logged in
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Logs out user
# Redirects to index page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Shows the user's saved designs
@app.route('/designs')
@login_required
def designs():
    return render_template('designs.html', title='My Designs') 

# Will email user with password reset information
# Not accessible if logged in
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        # message always displayed to prevent client from seeing which emails are registered
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                            title='Reset Password', form=form)

# If correct reset token, will allow user to reset password
# Not accessible if logged in
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
         return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_pasword.html', form=form)

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
