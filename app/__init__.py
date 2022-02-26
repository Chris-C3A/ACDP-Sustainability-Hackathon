import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # app.config.from_pyfile('src/config.py')
    app.config.from_object("config.Development")  # development config

    # print(app.config["SQLALCHEMY_DATABASE_URI"])
    # print(app.config["SECRET_KEY"])

    # init packages
    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register endpoint blueprints
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.post import post as post_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(post_blueprint, url_prefix="/post")


    return app
