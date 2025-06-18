import os
import sys
import uuid
import csv
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user_profile import UserProfile
from bandit_linucb import LinUCB
from payload_generator import generate_nudge_payload
from reporting import generate_user_report

app = Flask(__name__)

# ----------------- USER PRELOAD FROM METADATA -----------------
def preload_users_from_metadata(log_path="user_metadata_log.csv"):
    users = {}
    if not os.path.exists(log_path):
        print(f"[WARN] No metadata log found at {log_path}")
        return users

    with open(log_path, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("consent", "").lower() != "true":
                continue
            user_id = row["user_id"]
            try:
                profile_type = row.get("profile_type", "stress_eater")
                profile = UserProfile(profile_type=profile_type)
                bandit = LinUCB(num_arms=3, context_dim=5, alpha=0.1)
                users[user_id] = {"profile": profile, "bandit": bandit}
            except Exception as e:
                print(f"[ERROR] Failed to preload user {user_id}: {e}")
    print(f"[INFO] Preloaded {len(users)} users from metadata.")
    return users

users = preload_users_from_metadata()

# ----------------- USER REGISTRATION -----------------
@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        user_id = str(uuid.uuid4())
        data = request.get_json() or {}

        profile_type = data.get("profile_type", "stress_eater")
        users[user_id] = {
            "profile": UserProfile(profile_type=profile_type),
            "bandit": LinUCB(num_arms=3, context_dim=5, alpha=0.1)
        }

        metadata = {
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "consent": data.get("consent_flag", False),
            "age_range": data.get("age_range", "Unknown"),
            "gender": data.get("gender", "Unknown"),
            "ethnicity": data.get("ethnicity", "Unknown"),
            "profile_type": profile_type
        }

        log_path = "user_metadata_log.csv"
        is_new = not os.path.exists(log_path)
        with open(log_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=metadata.keys())
            if is_new:
                writer.writeheader()
            writer.writerow(metadata)

        return jsonify({"user_id": user_id})
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

# ----------------- STATE STREAMING -----------------
@app.route('/stream_state', methods=['POST'])
def stream_state():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if user_id not in users:
            return jsonify({"error": "Invalid user_id"}), 400

        state = data.get("state", {})
        timestamp = data.get("timestamp", datetime.now(timezone.utc).isoformat())

        log_path = "sensor_state_log.csv"
        is_new = not os.path.exists(log_path)
        with open(log_path, "a", newline="") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["timestamp", "user_id", "gps_lat", "gps_lon", "heart_rate", "sleep_hours", "steps"])
            writer.writerow([
                timestamp,
                user_id,
                *state.get("gps", [None, None]),
                state.get("heart_rate"),
                state.get("sleep_hours"),
                state.get("steps")
            ])

        return jsonify({"status": "state logged", "timestamp": timestamp})
    except Exception as e:
        return jsonify({"error": f"Stream state failed: {str(e)}"}), 500

# ----------------- NOTIFICATION -----------------
@app.route('/notify_user', methods=['POST'])
def notify_user():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if user_id not in users:
            return jsonify({"error": "Invalid user_id"}), 400

        user = users[user_id]["profile"]
        bandit = users[user_id]["bandit"]
        context = np.array(user.get_state_vector())

        arm = bandit.select_action(context)
        reward = user.respond_to_nudge(arm)
        bandit.update(context, arm, reward)
        engagement = round(user.engagement, 3)
        timestamp = datetime.now(timezone.utc).isoformat()

        with open("nudge_decision_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_id, arm, round(reward, 3), engagement, *[round(x, 3) for x in context]])

        return jsonify({
            "recommended_arm": arm,
            "context": context.tolist(),
            "reward": round(reward, 3),
            "engagement": engagement,
            "timestamp": timestamp
        })
    except Exception as e:
        return jsonify({"error": f"Notify failed: {str(e)}"}), 500

# ----------------- FEEDBACK -----------------
@app.route('/feedback', methods=['POST'])
def receive_feedback():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        arm = data.get("arm")
        accepted = data.get("accepted", False)

        if user_id not in users:
            return jsonify({"error": "Invalid user_id"}), 400

        engagement = round(users[user_id]["profile"].engagement, 3)
        timestamp = datetime.now(timezone.utc).isoformat()

        with open("nudge_feedback_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_id, arm, accepted, engagement])

        return jsonify({"status": "feedback logged", "timestamp": timestamp})
    except Exception as e:
        return jsonify({"error": f"Feedback failed: {str(e)}"}), 500

# ----------------- UTILITIES -----------------
@app.route('/generate_nudge_payload/<user_id>', methods=['GET'])
def get_nudge_payload(user_id):
    try:
        payload = generate_nudge_payload(user_id)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error": f"Failed to generate nudge: {str(e)}"}), 500

@app.route('/export_user_log/<user_id>', methods=['GET'])
def export_user_log(user_id):
    try:
        result = generate_user_report(user_id)
        return jsonify({"status": "success", "files": result})
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route('/user_ids', methods=['GET'])
def get_user_ids():
    return jsonify(sorted(users.keys()))

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/simulate')
def simulate_page():
    return render_template("simulate.html")

@app.route('/dashboard/data', methods=['GET'])
def dashboard_data():
    try:
        user_id = request.args.get("user_id")
        log = []

        if not os.path.exists("nudge_decision_log.csv"):
            return jsonify({"labels": [], "engagement": [], "rewards": [], "arms": []})

        with open("nudge_decision_log.csv", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "timestamp":
                    continue
                if user_id and row[1] != user_id:
                    continue
                log.append({
                    "timestamp": row[0],
                    "user_id": row[1],
                    "arm": int(row[2]),
                    "reward": float(row[3]),
                    "engagement": float(row[4])
                })

        return jsonify({
            "labels": [entry["timestamp"] for entry in log],
            "engagement": [entry["engagement"] for entry in log],
            "rewards": [entry["reward"] for entry in log],
            "arms": [entry["arm"] for entry in log]
        })
    except Exception as e:
        return jsonify({"error": f"Failed to load dashboard data: {str(e)}"}), 500

@app.route('/test_route', methods=['GET'])
def test_route():
    return "It works!"

if __name__ == '__main__':
    print("🚀 Launching KeyRD Flask app...")
    app.run(debug=True)
