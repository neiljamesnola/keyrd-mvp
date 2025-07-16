# app/routes/feedback.py

from flask import Blueprint, request, jsonify

from app.models import db, User, NudgeLog
from app.state import agent

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/feedback", methods=["POST"])
def feedback():
    """
    Logs user feedback (reward) for a previously sent nudge.
    Updates LinUCB agent accordingly.
    
    Expected JSON:
    {
        "email": "user@example.com",
        "nudge_id": 2,
        "reward": 1.0
    }
    """
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        arm = data.get("nudge_id")
        reward = data.get("reward")

        if not all([email, isinstance(arm, int), isinstance(reward, (int, float))]):
            return jsonify({"error": "Missing or invalid fields: email, nudge_id (int), reward (float)"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Find most recent unrewarded log for this nudge
        log = (
            NudgeLog.query.filter_by(user_id=user.id, nudge_id=arm, reward=None)
            .order_by(NudgeLog.timestamp.desc())
            .first()
        )

        if not log:
            return jsonify({"error": "No pending nudge log found to reward"}), 404

        # Apply feedback
        log.reward = reward
        db.session.commit()

        # Update RL model
        agent.update(arm, log.context_vector, reward)

        return jsonify({"status": "agent updated", "nudge_id": arm, "reward": reward})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
