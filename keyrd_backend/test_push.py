import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

# Token you saw on the device
token = "ExponentPushToken[ZugFNqAfvcByxquwcGyjTt]"

message = {
    "to": token,
    "sound": "default",
    "title": "KeyRD 🔔",
    "body": "Don't forget to grab your meal prep from the frig 🚀",
    "data": {"source": "Flask API"}
}

response = requests.post(EXPO_PUSH_URL, json=message)

print("Status:", response.status_code)
print("Response:", response.json())
