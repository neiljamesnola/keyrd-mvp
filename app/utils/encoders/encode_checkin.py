# file: utils/encoders/encode_checkin.py
import numpy as np

def encode_checkin(user_data):
    """
    Encodes self-reported daily state variables.
    Each is expected on a 1–5 scale and normalized to [0, 1].
    If missing, defaults to midpoint (0.5).
    """

    def norm(val):
        try:
            return (float(val) - 1) / 4.0
        except:
            return 0.5

    mood = norm(user_data.get("mood"))
    stress = norm(user_data.get("stress_level"))
    hunger = norm(user_data.get("hunger"))
    cravings = norm(user_data.get("cravings"))
    energy = norm(user_data.get("energy_level"))

    return np.array([mood, stress, hunger, cravings, energy])
