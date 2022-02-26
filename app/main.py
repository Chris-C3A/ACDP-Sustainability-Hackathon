from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def posts():
    posts=[(1,"Title1",'/static/avacad.jpg','LOL xD'),(2,"Title2",'/static/avacad.jpg', 'Funny Caption'),(3,"Title3",'/static/avacad.jpg', 'haha'),(4,"Title4",'/static/avacad.jpg','WasteWatchers Unite!')] #map(tuple,fetchall(QUERY))
    page = render_template('top.html')
    for post in posts:
        page += render_template('postGen.html', postID=post[0], title=post[1], imgUrl=post[2], caption=post[3])
    page += render_template('bottom.html')
    return page


@main.route('/profile')
def profile():
    return render_template('profile.html')
