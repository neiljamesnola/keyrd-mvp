import numpy as np
import random

def generate_context_vector(user_type="resilient"):
    hour = random.randint(0, 23)
    day = random.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    stage_of_change = random.choice([1, 2, 3, 4, 5])
    location = random.choice(["home", "gym", "store", "work", "clinic", "travel", "other"])
    last_nudge_type = random.choice(["reminder", "motivate", "educate", "reward", "none"])

    return {
        "context": {
            "steps": int(np.clip(np.random.normal(6000, 3000), 0, 20000)),
            "hr": round(np.random.normal(75, 10), 1),
            "sleep_quality": round(np.clip(np.random.normal(6.5, 1.5), 0, 10), 1),
            "sleep_duration": round(np.clip(np.random.normal(7.0, 1.0), 0, 12), 1),
            "hr_variability": round(np.random.normal(40, 10), 1),
            "stress": round(np.random.beta(2, 5), 3),
            "fatigue": round(np.random.beta(2, 5), 3),
            "motivation": round(np.random.beta(5, 2), 3),
            "goal_salience": round(np.random.uniform(0, 1), 3),
            "readiness": round(np.random.beta(4, 3), 3),
            "stage_of_change": stage_of_change,
            "location_type": location,
            "gps_cluster": random.choice(["cluster_1", "cluster_2", "cluster_3"]),
            "last_nudge_type": last_nudge_type,
            "nudge_history_vector": [random.randint(0, 4) for _ in range(5)],
            "emr_vector": [round(np.random.normal(0, 1), 3) for _ in range(8)],
            "has_diabetes": random.random() < 0.15,
            "has_hypertension": random.random() < 0.25,
            "num_meds": random.randint(0, 5),
            "recent_reward": round(np.random.uniform(0, 1), 3),
            "novelty_saturation": round(np.random.beta(2, 6), 3),
            "engagement": round(np.random.beta(5, 2), 3),
            "cumulative_reward": round(np.random.normal(20, 5), 2),
            "time_of_day": hour,
            "day_of_week": day,
            "com_b": {
                "capability": round(np.random.uniform(0.4, 1.0), 3),
                "opportunity": round(np.random.uniform(0.4, 1.0), 3),
                "motivation": round(np.random.uniform(0.3, 1.0), 3)
            }
        }
    }
