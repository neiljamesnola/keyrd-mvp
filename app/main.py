# app/main.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from app.routes import register_blueprints
from app.state import load_agent
from app.models import db  # ✅ Critical: use shared db instance from models.py


def create_app():
    # ───── App Initialization ─────
    app = Flask(__name__, instance_relative_config=True)

    # ───── Config Setup ─────
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "..", "instance", "keyrd.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ───── Extensions Init ─────
    db.init_app(app)

    # ───── Register Routes ─────
    register_blueprints(app)

    # ───── App Context Setup ─────
    with app.app_context():
        db.create_all()
        load_agent()

    return app
