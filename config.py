import os


class Development:
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_DATABASE_URI = "sqlite:///tmp/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
