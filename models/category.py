# models/category.py

from . import db

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), unique=True, nullable=False)

    hobbies = db.relationship('Hobby', backref='category', lazy=True)
