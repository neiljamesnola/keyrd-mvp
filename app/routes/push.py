# keyrd_mvp/app/routes/push.py

from flask import Blueprint, request, jsonify
from app.models import db, User, NudgeLog
from app.utils.context_vector import build_context_vector
from app.utils.push import send_push_notification
from app.state import agent as linucb, save_agent
import numpy as np

push_bp = Blueprint("push", __name__)

# ───── Helper: Parse JSON Safely ─────
def parse_json(force=True):
    try:
        return request.get_json(force=force)
    except Exception as e:
        raise ValueError(f"Invalid JSON payload: {str(e)}")

# ───── Route: Send Personalized Nudge ─────
@push_bp.route("/push", methods=["POST"])
def push():
    """Select and send a personalized nudge to the user via push notification."""
    try:
        data = parse_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing 'user_id' in request body"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} not found"}), 404

        context = build_context_vector(user.id)
        nudge_id = linucb.select_action(context)

        title = "Today’s Nudge"
        body = f"Try Nudge #{nudge_id + 1} today!"

        status_code, push_response = send_push_notification(
            user.device_token, title, body
        )

        db.session.add(NudgeLog(
            user_id=user.id,
            nudge_id=nudge_id,
            context_vector=context.tolist()
        ))
        db.session.commit()

        save_agent()

        return jsonify({
            "user_id": user.id,
            "nudge_id": nudge_id,
            "message": body,
            "push_status": status_code,
            "push_response": push_response
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ───── Route: Register or Update Device Token ─────
@push_bp.route("/push/register", methods=["POST"])
def register_push_token():
    """Register or update the device push token for a user."""
    try:
        data = parse_json()
        user_id = data.get("user_id")
        device_token = data.get("device_token")

        if not user_id or not device_token:
            return jsonify({"error": "Both 'user_id' and 'device_token' are required"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User {user_id} not found"}), 404

        user.device_token = device_token
        db.session.commit()

        return jsonify({"message": "Device token registered successfully"}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ───── Route: Manually Trigger Test Push ─────
@push_bp.route("/push/test", methods=["POST"])
def test_push():
    """Send a test push notification to a specified user."""
    try:
        data = parse_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing 'user_id' in request body"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} not found"}), 404

        status_code, push_response = send_push_notification(
            user.device_token,
            title="Test Notification",
            body="This is a test push notification from KeyRD 🚀"
        )

        return jsonify({
            "user_id": user.id,
            "message": "Test push notification sent",
            "push_status": status_code,
            "push_response": push_response
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ───── Route: List All Users (Debug Only) ─────
@push_bp.route("/users", methods=["GET"])
def list_users():
    """List all users with device tokens and emails (debug tool)."""
    try:
        users = User.query.all()
        return jsonify([
            {
                "id": user.id,
                "email": user.email,
                "device_token": user.device_token
            } for user in users
        ])
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
