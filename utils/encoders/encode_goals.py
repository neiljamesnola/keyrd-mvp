# file: utils/encoders/encode_goals.py
import numpy as np

def encode_goals(user_data):
    """
    Encodes goal_type and nudge_style into numeric features.
    """

    goal_type = user_data.get("goal_type", "").lower()
    nudge_style = user_data.get("nudge_style", "").lower()

    goal_map = {
        "weight_loss": 0.8,
        "lower_bp": 0.6,
        "better_labs": 0.7,
        "more_energy": 0.5,
        "better_mood": 0.4
    }
    nudge_map = {
        "gentle": 0.5,
        "motivating": 0.7,
        "directive": 1.0,
        "humorous": 0.6
    }

    goal_score = goal_map.get(goal_type, 0.3)
    nudge_score = nudge_map.get(nudge_style, 0.5)

    return np.array([goal_score, nudge_score])
