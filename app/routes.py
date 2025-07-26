from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Message
from . import db, login_manager
from datetime import timedelta

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('main.chat'))
        flash('Invalid credentials')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    q = request.args.get('q', '').lower()
    if request.method == 'POST':
        content = request.form['content']
        recipient_id = request.form.get('recipient')

        # Convert empty string to None (public message)
        recipient_id = int(recipient_id) if recipient_id else None

        new_msg = Message(content=content, user_id=current_user.id, recipient_id=recipient_id)
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for('main.chat'))  # redirect to avoid resubmission

    messages = Message.query.order_by(Message.timestamp.asc()).all()
    if q:
        messages = [m for m in messages if
                    q in m.content.lower() or
                    q in m.user.username.lower() or
                    (m.recipient and q in m.recipient.username.lower())]

    users = User.query.all()
    return render_template("chat.html", messages=messages, users=users, timedelta=timedelta)
