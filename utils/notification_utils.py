# app/utils/notification_utils.py

import requests
import json
import os

# Environment variables or config secrets
FCM_SERVER_KEY = os.getenv("FCM_SERVER_KEY")

def send_push_notification(device_token, title, body, data_payload=None):
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    message = {
        "to": device_token,
        "notification": {
            "title": title,
            "body": body,
            "sound": "default"
        },
        "priority": "high",
        "data": data_payload or {}
    }

    response = requests.post(url, headers=headers, data=json.dumps(message))
    return response.status_code, response.json()
