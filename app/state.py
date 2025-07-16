# app/state.py

from app.agents.bandit_linucb import LinUCB

# Configuration constants
NUM_NUDGES = 5
CONTEXT_DIM = 26
ALPHA = 0.1

# Always create a fresh LinUCB agent — no loading
agent = LinUCB(num_arms=NUM_NUDGES, context_dim=CONTEXT_DIM, alpha=ALPHA)

def load_agent():
    """No-op: we’re starting fresh each time."""
    print("[state.py] Skipping model load — using clean agent.")

def save_agent():
    """Optional: Save manually later if desired."""
    print("[state.py] Skipping model save — clean session only.")
