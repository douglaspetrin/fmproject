from flask import Flask
from fmapi.models import db
import os


def create_app():
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = os.getenv("FMAPI_SECRET_KEY", "top-secrete-key")
    flask_app.config["AUTH_TOKEN_EXPIRES_IN"] = int(os.getenv("AUTH_TOKEN_EXPIRES_IN", 3600))
    flask_app.config["LOG_TO_FILE"] = int(os.getenv("LOG_TO_FILE", 0))
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(
        os.getenv("DB_USER", "doug"),
        os.getenv("DB_PASSWORD", ""),
        os.getenv("DB_HOST", "mysql"),
        os.getenv("DB_NAME", "fmapi")
    )
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    return flask_app
