# models/hobby.py

from . import db

class Hobby(db.Model):
    __tablename__ = 'hobbys'

    hobby_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hobby = db.Column(db.String(255), unique=True, nullable=False)
    axis_x = db.Column(db.Integer, nullable=False)
    axis_y = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
 