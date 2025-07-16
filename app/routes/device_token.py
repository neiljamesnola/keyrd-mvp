# app/routes/device_token.py

from flask import Blueprint, request, jsonify
from ..models import db, User

device_token_bp = Blueprint("device_token", __name__)


@device_token_bp.route("/register_token", methods=["POST"])
def register_token():
    """
    Registers or updates a device token for a user.

    Expected JSON:
    {
        "email": "user@example.com",
        "device_token": "abcdef123456..."
    }
    """
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        token = data.get("device_token")

        if not email or not token:
            return jsonify({"error": "Missing email or device_token"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.device_token = token
        db.session.commit()

        return jsonify({"status": "Device token registered", "email": email})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
