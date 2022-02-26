from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def index():
    posts=[(1,"Title1",'/static/avacad.jpg','LOL xD'),(2,"Title2",'/static/avacad.jpg', 'Funny Caption'),(3,"Title3",'/static/avacad.jpg', 'haha'),(4,"Title4",'/static/avacad.jpg','WasteWatchers Unite!')] #map(tuple,fetchall(QUERY))
    page = render_template('postGen.html',posts=posts)
    return page


@main.route('/profile')
def profile():
    return render_template('profile.html')
