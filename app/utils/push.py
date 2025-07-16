# app/utils/push.py

import requests

def send_push_notification(token, title, body):
    """
    Sends a push notification using Expo Push API for ExponentPushToken[...] tokens.
    """
    if not token or not token.startswith("ExponentPushToken["):
        return 400, "Invalid Expo push token"

    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "to": token,
        "sound": "default",
        "title": title,
        "body": body,
        "priority": "high"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, f"Failed to send push notification: {str(e)}"
