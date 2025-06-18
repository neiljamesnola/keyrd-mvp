from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    device_token = db.Column(db.String(512), nullable=True)  # For APNs/FCM delivery

    def __repr__(self):
        return f"<User {self.email}>"

class NudgeLog(db.Model):
    __tablename__ = "nudge_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nudge_id = db.Column(db.Integer, nullable=False)
    context_vector = db.Column(JSON, nullable=False)
    reward = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("nudge_logs", lazy=True))

    def __repr__(self):
        return f"<NudgeLog user={self.user_id} nudge={self.nudge_id} reward={self.reward}>"
