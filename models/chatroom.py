from . import db
from datetime import datetime

class ChatRoom(db.Model):
    __tablename__ = 'chatrooms'
    
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    messages = db.relationship('Message', backref='room', lazy=True)
    participants = db.relationship('User', secondary='room_participants', backref='rooms')

class Message(db.Model):
    __tablename__ = 'messages'
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('chatrooms.room_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship('User', backref='messages')

# Association table for room participants
room_participants = db.Table('room_participants',
    db.Column('room_id', db.Integer, db.ForeignKey('chatrooms.room_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)