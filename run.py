import os
from venv import create
from app import db, create_app

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


app = create_app()


# run server with debug mode

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(host="0.0.0.0", debug=True, use_reloader=True, ssl_context='adhoc')
