import requests
import os

FCM_ENDPOINT = "https://fcm.googleapis.com/fcm/send"
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")  # Add this to .env

def send_push_notification(device_token, title, body, data_payload=None):
    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "to": device_token,
        "notification": {
            "title": title,
            "body": body,
        },
        "data": data_payload or {},
    }

    response = requests.post(FCM_ENDPOINT, json=payload, headers=headers)

    if response.status_code != 200:
        print("❌ Push failed:", response.status_code, response.text)
    return response.json()
