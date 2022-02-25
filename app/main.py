from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')
