from flask_socketio import emit
from flask_login import current_user
from datetime import datetime, timedelta
from .models import Message, User
from . import db, socketio

@socketio.on("send_message")
def handle_send_message(data):
    content = data.get("content", "")
    recipient_id = data.get("recipient_id")

    message = Message(
        user_id=current_user.id,
        content=content,
        recipient_id=recipient_id if recipient_id else None
    )
    db.session.add(message)
    db.session.commit()

    recipient_user = User.query.get(recipient_id) if recipient_id else None

    response = {
        "content": content,
        "sender_username": current_user.username,
        "recipient_username": recipient_user.username if recipient_user else None,
        "timestamp": (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
        "self": True
    }

    emit("receive_message", response)

    response["self"] = False

    emit("receive_message", response, broadcast=True, include_self=False)
