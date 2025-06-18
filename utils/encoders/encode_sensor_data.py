# file: utils/encoders/encode_sensor_data.py
import numpy as np

def encode_sensor_data(sensor_data):
    """
    Encodes passive data from wearable or phone sensors.
    Values should be pre-normalized or scaled here.
    If unavailable, defaults to neutral midpoints.
    """

    def safe(val, scale=1.0, default=0.5):
        try:
            return float(val) / scale
        except:
            return default

    steps_today = safe(sensor_data.get("steps_today"), scale=20000)
    steps_last_hour = safe(sensor_data.get("steps_last_hour"), scale=1000)
    sedentary_minutes = safe(sensor_data.get("sedentary_minutes"), scale=600)

    heart_rate = safe(sensor_data.get("heart_rate"), scale=200)
    resting_hr = safe(sensor_data.get("resting_hr"), scale=100)
    max_hr = safe(sensor_data.get("max_hr"), scale=220)

    sleep_minutes = safe(sensor_data.get("total_sleep_minutes"), scale=960)
    sleep_efficiency = safe(sensor_data.get("sleep_efficiency"), scale=100)

    return np.array([
        steps_today, steps_last_hour, sedentary_minutes,
        heart_rate, resting_hr, max_hr,
        sleep_minutes, sleep_efficiency
    ])
