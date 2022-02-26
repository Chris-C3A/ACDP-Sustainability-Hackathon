from flask import Blueprint, render_template, flash, jsonify, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import User, Post, Follow
from app.src.utils import get_coordinates_of_posts

main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def index():
    posts = [(1, "My Friday", '/static/stock1.jpg', 'LOL xD'), (2, "Your Monday", '/static/stock2.jpg', 'Funny Caption'), (3, "For the gram!",
                                                                                                                           '/static/stock3.jpg', 'haha'), (4, "Honestly", '/static/stock4.jpg', 'WasteWatchers Unite!')]  # map(tuple,fetchall(QUERY))
    page = render_template('postGen.html', posts=posts)
    return page


@main.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    # else:
    #     username
    #     email
    #     public

    #     current_user.username = username
    #     u

    #     db.session.commit()

# api request


@main.route('/findFriends', methods=['GET', 'POST'])
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


@main.route('/map/get_locations', methods=['GET', 'POST'])
def get_locations():
    if request.method == 'GET':
        # return render_template('/map/map.html')
        return render_template('map/maptest.html')
    elif request.method == 'POST':
        # query only post whose users are public
        posts = Post.query.all()

        # return in json format
        coordinates = get_coordinates_of_posts(posts)

        return jsonify(coordinates)
