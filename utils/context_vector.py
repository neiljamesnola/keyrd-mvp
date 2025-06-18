# file: utils/context_vector.py
import numpy as np

from utils.encoders.encode_demographics import encode_demographics
from utils.encoders.encode_diet_prefs import encode_diet_prefs
from utils.encoders.encode_goals import encode_goals
from utils.encoders.encode_schedule import encode_schedule
from utils.encoders.encode_device_meta import encode_device_meta
from utils.encoders.encode_checkin import encode_checkin
from utils.encoders.encode_sensor_data import encode_sensor_data

def build_context_vector(user_data, sensor_data=None):
    """
    Build the full context vector from onboarding + check-in + sensor data.
    """

    vector_parts = [
        encode_demographics(user_data),
        encode_diet_prefs(user_data),
        encode_goals(user_data),
        encode_schedule(user_data),
        encode_device_meta(user_data),
        encode_checkin(user_data),
        encode_sensor_data(sensor_data or {})  # fallback if None
    ]

    return np.concatenate(vector_parts).astype(np.float32)
