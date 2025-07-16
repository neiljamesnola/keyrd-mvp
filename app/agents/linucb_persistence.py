import os
from app.agents.bandit_linucb import LinUCB

# Default path for persisted model
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../instance/linucb_model.pkl")

def save_linucb_model(agent: LinUCB, filepath: str = DEFAULT_MODEL_PATH):
    """
    Save the state of a LinUCB model to disk.

    Args:
        agent (LinUCB): The LinUCB agent instance to persist.
        filepath (str): Destination file path for the model (pickle format).
    """
    try:
        agent.save(filepath)
        print(f"[LinUCB Save] Model persisted to: {filepath}")
    except Exception as e:
        print(f"[LinUCB Save Error] {e}")

def load_linucb_model(agent: LinUCB, filepath: str = DEFAULT_MODEL_PATH):
    """
    Load a previously saved LinUCB model into the given agent instance.

    Args:
        agent (LinUCB): The LinUCB agent to restore.
        filepath (str): Path to the persisted model file.
    """
    try:
        agent.load(filepath)
        print(f"[LinUCB Load] Model loaded from: {filepath}")
    except Exception as e:
        print(f"[LinUCB Load Error] {e}")
