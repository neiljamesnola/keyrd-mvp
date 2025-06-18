# file: utils/encoders/encode_diet_prefs.py
import numpy as np

def encode_diet_prefs(user_data):
    """
    Encode diet_type, food_allergies, and food_avoidances.
    Currently encodes only diet_type.
    """

    diet_type = user_data.get("diet_type", "").lower()
    # Example: simple diet_type encoding (expand as needed)
    diet_map = {
        "omnivore": 0.2,
        "vegetarian": 0.4,
        "vegan": 1.0,
        "pescatarian": 0.6,
        "dash": 0.8
    }
    diet_score = diet_map.get(diet_type, 0.5)  # default if unknown

    return np.array([diet_score])
