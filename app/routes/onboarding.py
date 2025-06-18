# file: app/routes/onboarding.py

from flask import Blueprint, request, jsonify
from app.models import db, User
import uuid

# ✅ This is the object your main.py is looking for:
onboarding_bp = Blueprint('onboarding', __name__)

@onboarding_bp.route('/submit_onboarding', methods=['POST'])
def submit_onboarding():
    try:
        data = request.get_json()

        # Generate a UUID and store the full user onboarding info
        new_user = User(id=str(uuid.uuid4()), **data)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
