# models/result.py

from . import db

class Result(db.Model):
    __tablename__ = 'results'

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    axis_x = db.Column(db.Integer, nullable=False)
    axis_y = db.Column(db.Integer, nullable=False)
