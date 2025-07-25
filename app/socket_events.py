from flask_socketio import emit
from . import socketio
from flask_login import current_user
from .models import db, Message
from datetime import datetime

@socketio.on('send_message')
def handle_send(data):
    content = data['content']
    msg = Message(content=content, user_id=current_user.id, timestamp=datetime.utcnow())
    db.session.add(msg)
    db.session.commit()
    emit('receive_message', {
        'username': current_user.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M')
    }, broadcast=True)
