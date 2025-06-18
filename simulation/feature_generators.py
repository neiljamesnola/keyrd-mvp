import numpy as np
import random

# 1. Demographics
def generate_demographics():
    return {
        "age": np.random.randint(18, 80),
        "sex": random.choice(["male", "female", "nonbinary"]),
        "socioeconomic_status": np.random.choice(["low", "medium", "high"], p=[0.3, 0.5, 0.2])
    }

# 2. GPS / Location
def generate_location_context():
    return {
        "gps_cluster": np.random.randint(0, 5),
        "location_type": np.random.choice(["home", "gym", "store", "work", "transit", "outdoor"]),
        "time_of_day": np.random.randint(0, 24),
        "day_of_week": np.random.randint(0, 7)
    }

# 3. Medical / EMR
def generate_medical_context():
    return {
        "has_diabetes": int(np.random.rand() < 0.2),
        "has_hypertension": int(np.random.rand() < 0.3),
        "num_meds": np.random.randint(0, 5),
        "emr_vector": np.random.normal(0, 1, 5)  # simplified PCA-style embedding
    }

# 4. Biosensor Time Series (Sleep, HR, Steps)
def generate_biosensor_signals():
    return {
        "steps_today": np.random.uniform(500, 15000),
        "hr": np.random.uniform(50, 120),
        "hr_variability": np.random.uniform(10, 100),
        "sleep_duration": np.random.uniform(3, 10),
        "sleep_quality": np.random.uniform(1, 10),
        "stress": np.random.beta(2, 5),  # skewed low
        "fatigue": np.random.beta(2, 3)
    }

# 5. Psychological / Behavioral Traits
def generate_behavioral_state():
    return {
        "motivation": np.random.uniform(0.3, 0.9),
        "readiness": np.random.uniform(0.3, 0.9),
        "goal_salience": np.random.uniform(0.2, 0.8),
        "stage_of_change": np.random.randint(1, 6),
        "com_b": {
            "capability": np.random.uniform(0.4, 0.9),
            "opportunity": np.random.uniform(0.4, 0.9),
            "motivation": np.random.uniform(0.3, 0.9)
        },
        "nudge_acceptance_rate": np.random.uniform(0.4, 0.9)
    }

# 6. External Contexts / Events
def generate_life_context():
    return {
        "holiday_flag": int(np.random.rand() < 0.05),
        "has_support_network": int(np.random.rand() < 0.7),
        "recent_life_event": np.random.choice([None, "illness", "vacation", "family_stress"], p=[0.7, 0.1, 0.1, 0.1])
    }
