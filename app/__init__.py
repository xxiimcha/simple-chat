from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

# Global instances
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'main.login'

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Register socket events
    from . import socket_events

    return app
