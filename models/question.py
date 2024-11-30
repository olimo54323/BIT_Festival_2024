# models/question.py

from . import db

class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), unique=True, nullable=False)
    axis = db.Column(db.String(1), nullable=False)
