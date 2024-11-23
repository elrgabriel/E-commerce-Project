from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(30), nullable = False)
    user_password = db.Column(db.String(12), nullable = False)
    user_name = db.Column(db.String(30), nullable = False)
    user_last_name = db.Column(db.String(30))
    user_address = db.Column(db.String(60))
    user_district = db.Column(db.String(20))