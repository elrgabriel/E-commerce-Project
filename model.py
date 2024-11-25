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

class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(70), nullable = False)
    product_price = db.Column(db.Integer, nullable = False)
    product_image = db.Column(db.String(100), nullable = False)