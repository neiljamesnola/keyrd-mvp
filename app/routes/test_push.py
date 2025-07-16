# app/routes/test_push.py

from flask import Blueprint, request, jsonify
from app.utils.push import send_push_notification
from app.models import User

test_push_bp = Blueprint("test_push", __name__)

@test_push_bp.route("/test_push", methods=["POST"])
def test_push():
    """
    Sends a test push notification to the device token associated with a user's email.

    Expected JSON:
    {
        "email": "user@example.com",
        "title": "Test Title",
        "body": "This is a test notification.",
        "data": {
            "foo": "bar"
        }
    }
    """
    data = request.get_json()
    email = data.get("email")
    title = data.get("title", "Default Title")
    body = data.get("body", "This is a test notification.")
    payload = data.get("data", {})

    if not email:
        return jsonify({"error": "Missing email"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.device_token:
        return jsonify({"error": "User not found or device token missing"}), 404

    status, response = send_push_notification(user.device_token, title, body, payload)
    return jsonify({"status": status, "response": response}), status
