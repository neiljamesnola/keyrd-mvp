# app/utils/context_vector.py

import numpy as np
from app.models import db, User


def normalize(val, min_val, max_val):
    """Min-max normalize value to [0, 1] range."""
    try:
        val = float(val)
    except (TypeError, ValueError):
        return 0.0
    return (val - min_val) / (max_val - min_val) if max_val != min_val else 0.0


def one_hot(index, length):
    """Return a one-hot encoded vector."""
    vec = [0] * length
    if isinstance(index, int) and 0 <= index < length:
        vec[index] = 1
    return vec


def build_context_vector(user_id: int) -> np.ndarray:
    """
    Builds a normalized context vector from user onboarding + mock dynamic data.

    Returns:
        np.ndarray: Feature vector for LinUCB agent
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    vector = []

    # ─────────────────────────────────────────────
    # 🎂 Age: Normalize (18–90)
    vector.append(normalize(user.age or 40, 18, 90))

    # 🧬 Sex: One-hot [male, female, other]
    sex = (user.sex or "other").lower()
    sex_vector = {
        "male": [1, 0, 0],
        "female": [0, 1, 0],
    }.get(sex, [0, 0, 1])
    vector.extend(sex_vector)

    # 🍽️ Diet Type: One-hot (omnivore, vegetarian, vegan, pescatarian, dash)
    diet_order = ["omnivore", "vegetarian", "vegan", "pescatarian", "dash"]
    diet_index = diet_order.index(user.diet_type.lower()) if user.diet_type and user.diet_type.lower() in diet_order else -1
    vector.extend(one_hot(diet_index, len(diet_order)))

    # 🎯 Goal Type: One-hot (weight_loss, lower_bp, better_labs, more_energy, better_mood)
    goal_order = ["weight_loss", "lower_bp", "better_labs", "more_energy", "better_mood"]
    goal_index = goal_order.index(user.goal_type.lower()) if user.goal_type and user.goal_type.lower() in goal_order else -1
    vector.extend(one_hot(goal_index, len(goal_order)))

    # 🔁 Stage of Change: One-hot (TTM model)
    stage_order = ["precontemplation", "contemplation", "preparation", "action", "maintenance"]
    stage_index = stage_order.index(user.readiness_stage.lower()) if user.readiness_stage and user.readiness_stage.lower() in stage_order else -1
    vector.extend(one_hot(stage_index, len(stage_order)))

    # 💊 Chronic Conditions: Count how many flags (T2D, HTN, etc.)
    condition_count = len(user.chronic_conditions.split(",")) if user.chronic_conditions else 0
    vector.append(normalize(condition_count, 0, 5))  # normalize to 5+ condition scale

    # 🧠 Nudge Style: One-hot (gentle, motivating, directive, humorous)
    style_order = ["gentle", "motivating", "directive", "humorous"]
    style_index = style_order.index(user.nudge_style.lower()) if user.nudge_style and user.nudge_style.lower() in style_order else -1
    vector.extend(one_hot(style_index, len(style_order)))

    # 🕓 Wake/Sleep Time → total sleep window (hours)
    try:
        sleep_duration = (datetime.combine(datetime.today(), user.sleep_time) -
                          datetime.combine(datetime.today(), user.wake_time)).seconds / 3600.0
        if sleep_duration < 0:  # wrap around midnight
            sleep_duration += 24
    except Exception:
        sleep_duration = 7
    vector.append(normalize(sleep_duration, 0, 12))

    # 🏙️ Work hours length
    try:
        start, end = user.work_hours.split("-")
        from datetime import datetime
        fmt = "%H:%M"
        hours = (datetime.strptime(end.strip(), fmt) - datetime.strptime(start.strip(), fmt)).seconds / 3600.0
    except Exception:
        hours = 8
    vector.append(normalize(hours, 0, 16))

    # 🌐 Zip Code → Drop for now or use later via SES mapping

    return np.array(vector, dtype=np.float32)
