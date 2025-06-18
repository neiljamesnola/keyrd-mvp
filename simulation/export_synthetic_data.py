import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from generate_context import generate_context_vector

OUTPUT_DIR = "results/synthetic/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_numpy(obj):
    """Recursively convert NumPy types to native Python types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def generate_synthetic_records(n=1000, user_type="resilient", seed=42):
    """Generate synthetic user interaction records with contextual metadata."""
    np.random.seed(seed)
    records = []

    for _ in range(n):
        context = generate_context_vector(user_type=user_type)
        record = {
            "user_id": f"{user_type}_{int(np.random.randint(1e6))}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": context,
            "action_taken": int(np.random.choice([0, 1, 2, 3])),
            "reward_received": float(np.round(np.random.uniform(0, 1), 3)),
            "done": bool(np.random.rand() < 0.01)
        }
        records.append(record)

    return records

if __name__ == "__main__":
    for user_type in ["resilient", "stress_eater", "fatigue_sensitive"]:
        print(f"🔁 Generating synthetic data for: {user_type}")
        synthetic_records = generate_synthetic_records(n=1000, user_type=user_type)

        jsonl_path = os.path.join(OUTPUT_DIR, f"{user_type}.jsonl")
        csv_path = os.path.join(OUTPUT_DIR, f"{user_type}.csv")

        with open(jsonl_path, "w") as f:
            for r in synthetic_records:
                f.write(json.dumps(convert_numpy(r)) + "\n")

        # Flatten context for easier tabular visualization
        flat_records = []
        for r in synthetic_records:
            flat = {
                "user_id": r["user_id"],
                "timestamp": r["timestamp"],
                "action_taken": r["action_taken"],
                "reward_received": r["reward_received"],
                "done": r["done"]
            }
            flat.update(r["context"])
            flat_records.append(flat)

        pd.DataFrame(flat_records).to_csv(csv_path, index=False)
        print(f"✅ Saved: {jsonl_path}")
        print(f"✅ Saved: {csv_path}")
