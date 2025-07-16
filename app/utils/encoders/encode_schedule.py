# file: utils/encoders/encode_schedule.py
import numpy as np
from datetime import datetime

def _time_to_float(time_str):
    """
    Converts time in HH:MM format to a float between 0 and 1.
    """
    try:
        t = datetime.strptime(time_str, "%H:%M")
        return (t.hour * 60 + t.minute) / 1440.0
    except:
        return 0.5  # default if malformed

def encode_schedule(user_data):
    """
    Encode wake_time, sleep_time, and work_hours.
    - wake/sleep are sin-normalized floats
    - work_hours becomes duration
    """

    wake = _time_to_float(user_data.get("wake_time", "07:00"))
    sleep = _time_to_float(user_data.get("sleep_time", "22:00"))

    work_hours = user_data.get("work_hours", "09:00-17:00")
    try:
        start, end = work_hours.split("-")
        work_start = _time_to_float(start.strip())
        work_end = _time_to_float(end.strip())
        duration = work_end - work_start
        if duration < 0:
            duration += 1.0  # wrap around midnight
    except:
        duration = 0.5  # fallback

    return np.array([wake, sleep, duration])
