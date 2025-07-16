import requests

url = "http://localhost:5000/push"

data = {
    "user_id": 1,  # Make sure this user exists in your database
    "context_vector": [0.1] * 26  # Replace with valid context input
}

try:
    response = requests.post(url, json=data)
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Non-JSON response body:", response.text)
except requests.exceptions.RequestException as e:
    print("Request failed:", str(e))
