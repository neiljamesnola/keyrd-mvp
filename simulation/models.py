from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

# Define the NudgeLog model
class NudgeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    nudge_type = db.Column(db.String(64), nullable=False)
    nudge_text = db.Column(db.Text, nullable=False)
    response = db.Column(db.String(64), nullable=False)
    reward = db.Column(db.Float, nullable=False)
    cumulative_reward = db.Column(db.Float, nullable=False)

# Define the FeedbackLog model
class FeedbackLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String(64), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)

# Factory pattern to avoid circular imports
def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', 'instance', 'keyrd.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
