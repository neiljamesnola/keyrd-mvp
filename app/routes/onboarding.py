# app/routes/onboarding.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models import db, User, NudgeLog
from ..utils.context_vector import build_context_vector
from ..utils.push import send_push_notification
from ..state import agent

# ✅ Define blueprint BEFORE any route decorators
onboarding_bp = Blueprint("onboarding", __name__)


@onboarding_bp.route("/submit_onboarding", methods=["POST"])
def submit_onboarding():
    """
    Handles full onboarding submission: stores structured data,
    triggers RL agent, logs nudge, sends push notification.
    """
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        device_token = data.get("device_token")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # 🔍 Lookup or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, created_at=datetime.utcnow())
            db.session.add(user)

        # 📥 Store static onboarding info
        user.device_token = device_token
        user.age = data.get("age")
        user.sex = data.get("sex")
        user.diet_type = data.get("diet_type")
        user.goal_type = data.get("goal_type")
        user.readiness_stage = data.get("readiness_stage")
        user.chronic_conditions = ",".join(data.get("chronic_conditions", []))
        user.nudge_style = data.get("nudge_style")
        user.work_hours = data.get("work_hours")
        user.zip_code = data.get("zip_code")

        # ⏰ Parse wake/sleep times
        try:
            if data.get("wake_time"):
                user.wake_time = datetime.strptime(data["wake_time"], "%H:%M").time()
            if data.get("sleep_time"):
                user.sleep_time = datetime.strptime(data["sleep_time"], "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid time format. Use HH:MM."}), 400

        db.session.commit()

        # 🧠 Compute context vector + select best nudge
        context_vector = build_context_vector(data)
        selected_nudge = agent.select_action(context_vector)

        # 📝 Log the decision
        log = NudgeLog(
            user_id=user.id,
            nudge_id=selected_nudge,
            context_vector=context_vector.tolist(),
            timestamp=datetime.utcnow(),
            reward=None
        )
        db.session.add(log)
        db.session.commit()

        # 🚀 Send push notification
        if user.device_token:
            send_push_notification(
                device_token=user.device_token,
                title="Your First Nudge",
                body=f"Nudge #{selected_nudge} is ready for you!",
                data_payload={"nudge_id": selected_nudge}
            )

        return jsonify({
            "success": True,
            "email": user.email,
            "nudge_id": selected_nudge
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
