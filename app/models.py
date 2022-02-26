# from turtle import title
from app import db
from flask import current_app
from flask_login import UserMixin
from app.src.constants import *
from datetime import datetime
import enum


class PrivacyEnum(enum.Enum):
    # Used to show whether a user profile is public or private
    public = True;
    private = False;

class User(UserMixin, db.Model):
    # Table name
    __tablename__ = 'user'

    # User info
    # (primary keys are required by SQLAlchemy)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_CHAR_LIMIT), unique=True)
    email = db.Column(db.String(EMAIL_CHAR_LIMIT), unique=True)
    password = db.Column(db.String(PASSWORD_CHAR_LIMIT))
    public = db.Column(db.Enum(PrivacyEnum), nullable=False)

    # For creating the User and Post one-to-many relationship
    posts = db.relationship("Post", back_populates="author")


class Post(db.Model):
    # Table name
    __tablename__ = 'post'

    # Post info
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(CAPTION_CHAR_LIMIT))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # For creating the User and Post one-to-many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    author = db.relationship("User", back_populates="posts")

    # For creating the Post and votes one-to-many relationship
    votes = db.relationship("Vote")


class VoteEnum(enum.Enum):
    # Used to show whether a user has upvoted or downvoted a post
    upvote = True
    downvote = False


class Vote(db.Model):
    # Table name
    __tablename__ = 'vote'

    # (primary keys are required by SQLAlchemy)
    id = db.Column(db.Integer, primary_key=True)

    # For creating the Post and votes one-to-many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    # Uses an enum to represent true or false
    upvoted = db.Column(db.Enum(VoteEnum), nullable=False)


class Follow(db.Model):
    # Table name
    __tablename__ = 'following'

    # (primary keys are required by SQLAlchemy)
    id = db.Column(db.Integer, primary_key=True)

    # For creating the User and follows one-to-many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'))
