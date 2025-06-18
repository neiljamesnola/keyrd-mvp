def generate_mock_user_context():
    return {
        "steps": np.random.randint(500, 15000),
        "hr": np.random.uniform(55, 100),
        "sleep_quality": np.random.uniform(4.0, 9.0),
        "sleep_duration": np.random.uniform(4, 9),
        "hr_variability": np.random.uniform(20, 80),
        "stress": np.random.uniform(0.1, 0.9),
        "fatigue": np.random.uniform(0.1, 0.9),
        "motivation": np.random.uniform(0.1, 1.0),
        "goal_salience": np.random.uniform(0.2, 1.0),
        "readiness": np.random.uniform(0.2, 1.0),
        "stage_of_change": np.random.randint(1, 6),
        "location_type": random.choice(["home", "gym", "store", "work"]),
        "has_diabetes": bool(random.getrandbits(1)),
        "has_hypertension": bool(random.getrandbits(1)),
        "num_meds": np.random.randint(0, 5),
        "recent_reward": np.random.uniform(0, 1),
        "novelty_saturation": np.random.uniform(0, 1),
        "gps_cluster": random.choice(["cluster_A", "cluster_B", "cluster_C"]),
        "emr_vector": [random.randint(0, 1) for _ in range(8)]  # binary features
    }
