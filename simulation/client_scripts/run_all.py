import subprocess
import time
import os

def run_script(script_name):
    print(f"\n🚀 Running: {script_name}")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Errors/Warnings:\n", result.stderr)

# Step 1: Register a new user and capture the user_id
print("🔐 Registering user...")
import requests
response = requests.post("http://127.0.0.1:5000/register_user", json={"consent_flag": True})
user_id = response.json().get("user_id")
print(f"✅ User registered: {user_id}")

# Save user_id for subsequent calls
with open("client_scripts/current_user_id.txt", "w") as f:
    f.write(user_id)

# Step 2: Stream state
print("📡 Sending sensor data...")
stream_payload = {
    "user_id": user_id,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "state": {
        "gps": [30.411, -91.183],
        "heart_rate": 78,
        "sleep_hours": 6.5,
        "steps": 3200
    }
}
response = requests.post("http://127.0.0.1:5000/stream_state", json=stream_payload)
print("📝 State stream response:", response.status_code, response.json())

# Step 3: Notify user
print("🔔 Triggering nudge...")
response = requests.post("http://127.0.0.1:5000/notify_user", json={"user_id": user_id})
notify_data = response.json()
print("📬 Notify response:", response.status_code, notify_data)

# Step 4: Send feedback
print("💬 Sending feedback...")
feedback_payload = {
    "user_id": user_id,
    "arm": notify_data.get("recommended_arm", 0),
    "accepted": True
}
response = requests.post("http://127.0.0.1:5000/feedback", json=feedback_payload)
print("📥 Feedback response:", response.status_code, response.json())

# Step 5: Export logs
print("📦 Exporting user report...")
response = requests.get(f"http://127.0.0.1:5000/export_user_log/{user_id}")
print("📤 Export response:", response.status_code, response.json())

# Step 6: Preview logs locally
run_script("client_scripts/preview_logs.py")
