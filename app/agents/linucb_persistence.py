# KeyRD MVP Launch - Phase-Integrated Main App

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

from app.utils.context_vector import build_context_vector
from app.agents.bandit_linucb import LinUCB
from app.agents.linucb_persistence import save_linucb_model, load_linucb_model

# ─────────────────────────────────────────────
# 🔧 App Setup
# ─────────────────────────────────────────────
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'instance', 'keyrd.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# 📦 Models
# ─────────────────────────────────────────────
from app.models import User, NudgeLog

# ─────────────────────────────────────────────
# 🧠 RL Agent Setup
# ─────────────────────────────────────────────
NUM_NUDGES = 5
CONTEXT_DIM = 30
agent = LinUCB(num_arms=NUM_NUDGES, context_dim=CONTEXT_DIM, alpha=0.1)
load_linucb_model(agent)

# ─────────────────────────────────────────────
# 📥 Onboarding + Nudge Selection
# ─────────────────────────────────────────────
@app.route("/submit_onboarding", methods=["POST"])
def submit_onboarding():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    user_data = data.copy()
    context_vector = build_context_vector(user_data)

    nudge_id = agent.select_action(context_vector)

    log = NudgeLog(
        user_id=user.id,
        nudge_id=nudge_id,
        context_vector=context_vector.tolist(),
        timestamp=datetime.utcnow(),
        reward=None
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"email": email, "nudge_id": nudge_id})

# ─────────────────────────────────────────────
# 🔁 Feedback Update
# ─────────────────────────────────────────────
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    email = data.get("email")
    nudge_id = data.get("nudge_id")
    reward = data.get("reward")

    if not all([email, nudge_id is not None, reward is not None]):
        return jsonify({"error": "Missing fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    log = NudgeLog.query.filter_by(user_id=user.id, nudge_id=nudge_id, reward=None)\
                          .order_by(NudgeLog.timestamp.desc()).first()
    if not log:
        return jsonify({"error": "Matching nudge log not found"}), 404

    log.reward = reward
    db.session.commit()

    agent.update(nudge_id, log.context_vector, reward)
    save_linucb_model(agent)

    return jsonify({"status": "agent updated"})

# ─────────────────────────────────────────────
# 🚀 Run App
# ─────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
