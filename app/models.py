# app/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

# ───── Shared DB Instance ─────
db = SQLAlchemy()

# ───── User Table ─────
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    device_token = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Static onboarding inputs
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    diet_type = db.Column(db.String(50))
    goal_type = db.Column(db.String(50))
    readiness_stage = db.Column(db.String(50))
    chronic_conditions = db.Column(db.Text)  # comma-separated for now
    nudge_style = db.Column(db.String(20))
    wake_time = db.Column(db.Time)
    sleep_time = db.Column(db.Time)
    work_hours = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))

    # Relationship to nudge logs
    logs = db.relationship("NudgeLog", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# ───── Nudge Log Table ─────
class NudgeLog(db.Model):
    __tablename__ = "nudge_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    nudge_id = db.Column(db.Integer, nullable=True)
    goal = db.Column(db.String(256), nullable=True)
    message = db.Column(db.String(512), nullable=True)
    context_vector = db.Column(JSON, nullable=True)
    reward = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NudgeLog user_id={self.user_id} timestamp={self.timestamp}>"
