# app/__init__.py

from flask import Flask
from config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 📦 Initialize extensions
    db.init_app(app)

    # 🔗 Register all route blueprints
    with app.app_context():
        from app.routes import register_blueprints
        register_blueprints(app)

    return app
