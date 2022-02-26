from flask import Blueprint, render_template, flash, Flask, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
mapViewer = Flask(__name__)


@main.route('/')  # home page that return 'index'
def index():
    posts = [(1, "My Friday", '/static/stock1.jpg', 'LOL xD'), (2, "Your Monday", '/static/stock2.jpg', 'Funny Caption'), (3, "For the gram!",
                                                                                                                           '/static/stock3.jpg', 'haha'), (4, "Honestly", '/static/stock4.jpg', 'WasteWatchers Unite!')]  # map(tuple,fetchall(QUERY))
    page = render_template('postGen.html', posts=posts)
    return page


@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/map')
def map_func():
	return render_template('map.html')