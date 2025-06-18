import random
import json
import os
from hashlib import sha256

# --- Constants ---
NUDGE_TYPES = ["notification", "email", "sms"]
Q_FILE = "output/q_data.json"
Q = {}  # Q-table dictionary: {state_hash: {action: value}}

# --- State Encoding ---
def hash_state(state):
    """Create a consistent hash for a dictionary state."""
    return sha256(json.dumps(state, sort_keys=True).encode()).hexdigest()

def get_state_key(state):
    return hash_state(state)

# --- Q-Value Logic ---
def get_q_value(state_key, action):
    return Q.get(state_key, {}).get(action, 0.0)

def set_q_value(state_key, action, value):
    if state_key not in Q:
        Q[state_key] = {}
    Q[state_key][action] = value

def update_q_value(state, action, reward, alpha=0.1):
    """Incremental Q-value update."""
    key = get_state_key(state)
    old = get_q_value(key, action)
    new = (1 - alpha) * old + alpha * reward
    set_q_value(key, action, round(new, 4))

def save_q_data(filepath=Q_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(Q, f, indent=2)

def load_q_data(filepath=Q_FILE):
    global Q
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            Q = json.load(f)

# --- Nudge Strategy ---
def choose_nudge(state, strategy="random", epsilon=0.1):
    key = get_state_key(state)

    if strategy == "random" or key not in Q:
        return random.choice(NUDGE_TYPES)

    if strategy == "epsilon_greedy":
        if random.random() < epsilon:
            return random.choice(NUDGE_TYPES)
        return max(Q[key], key=Q[key].get, default=random.choice(NUDGE_TYPES))

    raise ValueError(f"Unknown strategy: {strategy}")

# --- Nudge Messaging ---
def get_random_nudge_text(nudge_type):
    messages = {
        "notification": [
            "Time for a healthy snack?",
            "Take a quick break and stretch.",
            "How about a short walk?"
        ],
        "email": [
            "Check your weekly nutrition goal!",
            "New tips just arrived in your inbox.",
            "See how your habits are evolving."
        ],
        "sms": [
            "Stay hydrated 💧",
            "Meal prep tonight? You got this.",
            "Keep going—you’re doing great!"
        ]
    }
    return random.choice(messages.get(nudge_type, ["Default message."]))

# --- Response Simulation ---
def simulate_response(nudge_type, state):
    time_of_day = state.get("time_of_day")
    energy = state.get("energy_level")
    engagement = state.get("engagement")

    prob = 0.1
    if nudge_type == "notification":
        if time_of_day == "morning" and energy == "high":
            prob += 0.4
        if engagement == "high":
            prob += 0.2
    elif nudge_type == "sms":
        if engagement == "medium":
            prob += 0.3
    elif nudge_type == "email":
        if time_of_day == "evening":
            prob += 0.2

    return "accepted" if random.random() < prob else "ignored"

# --- Reward Shaping ---
def get_reward(response, nudge_type, state):
    base = 1.0 if response == "accepted" else -0.1

    mod = 0.0
    if nudge_type == "notification" and state.get("time_of_day") == "morning":
        mod += 0.1
    if state.get("engagement") == "high":
        mod += 0.2
    if response == "ignored" and state.get("energy_level") == "low":
        mod -= 0.2

    return round(base + mod, 2)

# --- Load on Import ---
load_q_data()
