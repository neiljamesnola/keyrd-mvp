from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests
import json

from app.utils.context_vector import build_context_vector
from app.agents.bandit_linucb import LinUCB
from app.models import User, NudgeLog

# ─────────────────────────────────────────────
# 🔧 App Setup
# ─────────────────────────────────────────────
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'instance', 'keyrd.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# 🧠 RL Agent Setup
# ─────────────────────────────────────────────
NUM_NUDGES = 5
CONTEXT_DIM = 30  # Update based on your vector size
agent = LinUCB(num_arms=NUM_NUDGES, context_dim=CONTEXT_DIM, alpha=0.1)

# ─────────────────────────────────────────────
# 🔔 Push Notification Utility
# ─────────────────────────────────────────────
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")

def send_push_notification(device_token, title, body, data_payload=None):
    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }
    message = {
        "to": device_token,
        "notification": {
            "title": title,
            "body": body,
            "sound": "default"
        },
        "priority": "high",
        "data": data_payload or {}
    }
    res = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(message))
    return res.status_code, res.json()

# ─────────────────────────────────────────────
# 📥 Onboarding + Nudge Assignment
# ─────────────────────────────────────────────
@app.route("/submit_onboarding", methods=["POST"])
def submit_onboarding():
    data = request.get_json()
    email = data.get("email")
    device_token = data.get("device_token")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    if device_token:
        user.device_token = device_token
        db.session.commit()

    context_vector = build_context_vector(data)
    selected_nudge = agent.select_action(context_vector)

    log = NudgeLog(
        user_id=user.id,
        nudge_id=selected_nudge,
        context_vector=context_vector.tolist(),
        timestamp=datetime.utcnow(),
        reward=None
    )
    db.session.add(log)
    db.session.commit()

    if user.device_token:
        send_push_notification(
            user.device_token,
            title="Today's Recommendation",
            body=f"Nudge #{selected_nudge} has been selected for you!",
            data_payload={"nudge_id": selected_nudge}
        )

    return jsonify({"email": email, "nudge_id": selected_nudge})

# ─────────────────────────────────────────────
# 🔁 Feedback (Reward Signal)
# ─────────────────────────────────────────────
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    email = data.get("email")
    arm = data.get("nudge_id")
    reward = data.get("reward")

    if email is None or arm is None or reward is None:
        return jsonify({"error": "Missing fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    log = NudgeLog.query.filter_by(user_id=user.id, nudge_id=arm, reward=None)\
                        .order_by(NudgeLog.timestamp.desc()).first()

    if not log:
        return jsonify({"error": "No matching nudge log found"}), 404

    log.reward = reward
    db.session.commit()

    agent.update(arm, log.context_vector, reward)

    return jsonify({"status": "agent updated"})

# ─────────────────────────────────────────────
# 📱 Device Token Registration
# ─────────────────────────────────────────────
@app.route("/register_device", methods=["POST"])
def register_device():
    data = request.get_json()
    email = data.get("email")
    device_token = data.get("device_token")

    if not email or not device_token:
        return jsonify({"error": "Missing email or device token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.device_token = device_token
    db.session.commit()
    return jsonify({"status": "device registered"})

# ─────────────────────────────────────────────
# 🧪 Init DB + Run App
# ─────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
