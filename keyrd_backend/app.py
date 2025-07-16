from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sqlite3
import os

from utils.register import save_device_token  # Preserves your current logic

app = Flask(__name__)
CORS(app)

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

@app.route("/")
def index():
    return jsonify({"message": "KeyRD Flask backend is running."})

# === Register device push token ===
@app.route("/api/push/register", methods=["POST"])
def register_push_token():
    data = request.get_json()
    user_id = data.get("user_id")
    token = data.get("token")

    if not user_id or not token:
        return jsonify({"error": "Missing user_id or token"}), 400

    # Save using your existing logic
    save_device_token(user_id, token)

    # Optionally persist in local SQLite (dev only)
    try:
        conn = sqlite3.connect("tokens.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tokens (user_id TEXT, token TEXT)")
        cursor.execute("INSERT INTO tokens (user_id, token) VALUES (?, ?)", (user_id, token))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ SQLite error: {e}")

    return jsonify({"success": True, "message": "Token registered."})


# === Send a test push notification ===
@app.route("/api/push/test", methods=["POST"])
def send_test_push():
    data = request.get_json()
    expo_token = data.get("expo_token")
    message = data.get("message", "🚀 Hello from KeyRD backend!")

    if not expo_token:
        return jsonify({"error": "Missing expo_token"}), 400

    payload = {
        "to": expo_token,
        "sound": "default",
        "title": "KeyRD Alert",
        "body": message,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(EXPO_PUSH_URL, json=payload, headers=headers)
        response.raise_for_status()
        return jsonify({"success": True, "response": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
