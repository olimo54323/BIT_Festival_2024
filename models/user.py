# models/user.py

from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

    results = db.relationship('Result', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)
