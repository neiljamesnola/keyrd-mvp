import json
import requests
import csv
from datetime import datetime, timezone

# Load most recent consenting user ID from metadata log
def get_latest_user_id(log_path="user_metadata_log.csv"):
    try:
        with open(log_path, newline='') as f:
            reader = list(csv.DictReader(f))
            consenting = [r for r in reader if r.get("consent", "").lower() == "true"]
            if not consenting:
                raise ValueError("No consenting users found in metadata.")
            return consenting[-1]["user_id"]
    except Exception as e:
        raise RuntimeError(f"Failed to read user ID: {e}")

user_id = get_latest_user_id()

# Construct payload
payload = {
    "user_id": user_id,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "state": {
        "gps": [30.4121, -91.1838],
        "heart_rate": 68,
        "sleep_hours": 7.2,
        "steps": 3200
    }
}

# Send POST request
response = requests.post(
    url="http://127.0.0.1:5000/stream_state",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Output result
print(f"Status Code: {response.status_code}")
print("Response:", response.json())
