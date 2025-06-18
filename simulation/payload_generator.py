# === Update to payload_generator.py ===

import uuid
import datetime
import random
import csv
import os


def generate_user_state():
    return {
        "fatigue": round(random.uniform(0.5, 0.9), 2),
        "stress": round(random.uniform(0.2, 0.6), 2),
        "engagement": round(random.uniform(0.6, 0.95), 2)
    }


def select_nudge_template():
    return {
        "text": "Feeling tired? Refuel with something light and steady.",
        "product": "Store-brand Greek yogurt + banana",
        "metadata": {
            "protein": "14g",
            "glycemic_index": "low",
            "estimated_cost": "$2.80"
        }
    }


def generate_nudge_payload(user_id):
    user_state = generate_user_state()
    suggestion = select_nudge_template()
    nudge_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    actions = [
        "Add to grocery list",
        "Find it nearby",
        "Remind me in 30 min"
    ]

    payload = {
        "nudge_id": nudge_id,
        "timestamp": timestamp,
        "user_id": user_id,
        "user_state": user_state,
        "suggestion": suggestion,
        "actions": actions
    }

    # Log the payload for audit/export
    log_path = "nudge_decision_log.csv"
    header = ["timestamp", "user_id", "nudge_id", "text", "product", "fatigue", "stress", "engagement"]

    file_exists = os.path.isfile(log_path)
    with open(log_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([
            timestamp,
            user_id,
            nudge_id,
            suggestion["text"],
            suggestion["product"],
            user_state["fatigue"],
            user_state["stress"],
            user_state["engagement"]
        ])

    return payload
