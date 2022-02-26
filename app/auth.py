from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        if not user:
            flash('Please sign up before!', 'danger')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)

        flash('successfully logged in', 'success')
        return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'danger')
            return redirect(url_for('auth.signup'))

        # if this returns a user, then the username already exists in database
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash('Passwords dont match', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=username,
                        password=generate_password_hash(password, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash("registered successfully", 'success')
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
