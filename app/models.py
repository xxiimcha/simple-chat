from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    sent_messages = db.relationship(
        'Message',
        foreign_keys='Message.user_id',
        backref='user',
        lazy=True
    )
    received_messages = db.relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        backref='recipient',
        lazy=True
    )

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)    
