from sqlalchemy import Column, Integer, String
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    email = Column(String(100), unique=True)
    password = Column(String(150))
