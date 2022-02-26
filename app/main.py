from flask import Blueprint, render_template, flash, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import null
from .models import *
from app import db

from app import db
from app.models import User, Post, Follow
from app.src.utils import get_coordinates_of_posts

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = render_template('index.html')
    return page


@main.route('/feed', methods=['GET', 'POST'])  # display posts
def feed():
    if request.method == 'GET':
        posts = []
        votes = []
        index = 0
        for record in Follow.query.filter_by(user_id=current_user.get_id()):
            for post in (Post.query.filter_by(user_id=record.following_id).order_by(Post.created_at).all()):
                votes.append(0)
                for voteRecord in Vote.query.filter_by(post_id=post.id):
                    if (voteRecord.upvoted == VoteEnum.upvote):
                        votes[index] += 1
                    elif (voteRecord.upvoted == VoteEnum.downvote):
                        votes[index] -= 1
                posts.append(post)
                index += 1
        posts.sort(key=lambda l:l.created_at, reverse=True)
        page = render_template('postGen.html', posts=posts, votes=votes)
        return page
    else:
        vote1 = request.form.get('Up')
        vote2 = request.form.get('Down')
        new_vote = None
        if (vote1 is not None):
            record = Vote.query.filter_by(post_id=vote1).filter_by(user_id=current_user.get_id()).first()
            if (record is not None):
                record.upvoted=VoteEnum.upvote
            else:
                new_vote = Vote(user_id=current_user.get_id(), post_id=vote1, upvoted=VoteEnum.upvote)
        elif (vote2 is not None):
            record = Vote.query.filter_by(post_id=vote2).filter_by(user_id=current_user.get_id()).first()
            if (record is not None):
                record.upvoted=VoteEnum.downvote
            else:
                new_vote = Vote(user_id=current_user.get_id(), post_id=vote2, upvoted=VoteEnum.downvote)
        if (new_vote is not None):
            db.session.add(new_vote)
        db.session.commit()
        return redirect('/feed')

@main.route('/explore', methods=['GET', 'POST'])
def exploreFeed():
    posts = []
    for record in User.query.filter_by(public=PrivacyEnum.public).all():
        for post in (Post.query.filter_by(user_id=record.id).order_by(Post.created_at).all()):
            posts.append(post)
    posts.sort(key=lambda l:l.created_at, reverse=True)
    page = render_template('postGen.html', posts=posts)
    return page

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    posts = []
    for post in (Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at).all()):
        posts.append(post)
    posts.sort(key=lambda l:l.created_at, reverse=True)
    followers = len(Follow.query.filter_by(following_id=current_user.get_id()).all())
    following = len(Follow.query.filter_by(user_id=current_user.get_id()).all())
    page = render_template('profile.html', posts=posts, followers=followers, following=following,
                            numberOfPosts=len(posts))
    return page
        

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
