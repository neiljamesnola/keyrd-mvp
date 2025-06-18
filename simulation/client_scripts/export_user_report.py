import requests
import csv

def get_latest_user_id(log_path="user_metadata_log.csv"):
    with open(log_path, newline='') as f:
        reader = list(csv.DictReader(f))
        consenting = [r for r in reader if r.get("consent", "").lower() == "true"]
        if not consenting:
            raise RuntimeError("No consenting user found.")
        return consenting[-1]["user_id"]

user_id = get_latest_user_id()

response = requests.get(f"http://127.0.0.1:5000/export_user_log/{user_id}")
print(f"Status Code: {response.status_code}")
print("Response:", response.json())
