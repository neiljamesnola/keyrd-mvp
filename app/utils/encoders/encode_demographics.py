# file: utils/encoders/encode_demographics.py
import numpy as np

def encode_demographics(user_data):
    """
    Encodes age, sex, and zip_code.
    - age is normalized
    - sex is one-hot: [male, female, other]
    - zip_code is dropped (placeholder)
    """

    # Normalize age to 0–1 range (assume 100 as upper cap)
    age = float(user_data.get("age", 0)) / 100.0

    sex = user_data.get("sex", "").lower()
    sex_encoded = {
        "male": [1.0, 0.0, 0.0],
        "female": [0.0, 1.0, 0.0],
    }.get(sex, [0.0, 0.0, 1.0])  # all other cases → "other"

    return np.array([age] + sex_encoded)
