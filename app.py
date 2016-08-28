from flask import Flask
from flask_bcrypt import Bcrypt
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Andreea98@localhost/websitedb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, db

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        email = form.email.data
        user = User(username, password, email, False)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Logged in successfully!')
                return redirect(url_for('index'))
	return render_template('login.html', form=form)	