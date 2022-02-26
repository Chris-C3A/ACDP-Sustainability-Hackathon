# from urllib import request
from app.models import Follow
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from .models import User
from app import db

main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def index():
    posts = [(1, "My Friday", '/static/stock1.jpg', 'LOL xD'), (2, "Your Monday", '/static/stock2.jpg', 'Funny Caption'), (3, "For the gram!",
                                                                                                                           '/static/stock3.jpg', 'haha'), (4, "Honestly", '/static/stock4.jpg', 'WasteWatchers Unite!')]  # map(tuple,fetchall(QUERY))
    page = render_template('postGen.html', posts=posts)
    return page


@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/findFriends', methods=['GET','POST'])
@login_required
def follow():
    if request.method == 'GET':
        return render_template('follow.html')
    else:
        usernameToFollow = request.form.get('username')

        # check if username to follow is in database and then follow
        user = User.query.filter_by(username=usernameToFollow).first()

        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('main.follow'))

        follow = Follow(user_id=current_user.id, following_id=user.id)

        # Add the follow relationship to the db
        db.session.add(follow)
        db.session.commit()

        flash(f'You are now following {user.username}!', 'success')
        return redirect(url_for('main.follow'))
