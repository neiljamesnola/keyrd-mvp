import json
import os

def save_device_token(user_id, token):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'device_tokens.json')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[str(user_id)] = token

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return True
