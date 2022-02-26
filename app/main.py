from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = render_template('index.html')
    return page


@main.route('/feed')  # display posts
def feed():
    posts = [(1, "User1", '/static/stock1.jpg', 'LOL xD'), (2, "User2", '/static/stock2.jpg', 'Funny Caption'), (3, "User3",'/static/stock3.jpg', 'haha'), (4, "User1", '/static/stock4.jpg', 'WasteWatchers Unite!')]  # map(tuple,fetchall(QUERY))
    page = render_template('postGen.html', posts=posts)
    return page
@main.route('/explore')
def exploreFeed():
    posts = [(1, "User1", '/static/stock1.jpg', 'LOL xD'), (2, "User2", '/static/stock2.jpg', 'Funny Caption'), (3, "User3",'/static/stock3.jpg', 'haha'), (4, "User1", '/static/stock4.jpg', 'WasteWatchers Unite!')]  # map(tuple,fetchall(QUERY))
    page = render_template('postGen.html', posts=posts)
    return page

@main.route('/profile')
def profile():
    return render_template('profile.html')
