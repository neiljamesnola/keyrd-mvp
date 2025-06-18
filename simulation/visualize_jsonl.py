import json
import pandas as pd
import matplotlib.pyplot as plt
from collections.abc import Iterable

def parse_jsonl_to_df(filepath):
    """
    Load a JSONL file into a pandas DataFrame, flattening nested context.
    """
    records = []
    with open(filepath, "r") as f:
        for line in f:
            data = json.loads(line)
            flat = {
                "user_id": data["user_id"],
                "timestamp": data["timestamp"],
                "action_taken": data["action_taken"],
                "reward_received": data["reward_received"],
                "done": data["done"],
            }
            context = data.get("context", {})
            for k, v in context.items():
                if isinstance(v, dict):
                    for sub_k, sub_v in v.items():
                        flat[f"{k}_{sub_k}"] = sub_v
                elif isinstance(v, Iterable) and not isinstance(v, str):
                    flat[k] = str(v)
                else:
                    flat[k] = v
            records.append(flat)
    return pd.DataFrame(records)


def plot_basic_diagnostics(df, title_prefix=""):
    """
    Plot basic distributions and trends in the dataset.
    """
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"{title_prefix} - Diagnostics", fontsize=16)

    # Reward distribution
    axs[0, 0].hist(df["reward_received"], bins=20, color="skyblue", edgecolor="black")
    axs[0, 0].set_title("Reward Distribution")

    # Engagement (if available)
    if "engagement" in df.columns:
        axs[0, 1].hist(df["engagement"], bins=20, color="lightgreen", edgecolor="black")
        axs[0, 1].set_title("Engagement Distribution")
    else:
        axs[0, 1].axis("off")

    # Reward over time
    axs[1, 0].plot(df["timestamp"], df["reward_received"], marker="o", linestyle="-", alpha=0.5)
    axs[1, 0].set_title("Reward Over Time")
    axs[1, 0].tick_params(axis="x", rotation=45)

    # Context variable of interest (e.g., fatigue if present)
    context_col = None
    for col in ["fatigue", "stress", "motivation"]:
        if col in df.columns:
            context_col = col
            break

    if context_col:
        axs[1, 1].plot(df["timestamp"], df[context_col], color="orange", marker="o", linestyle="-", alpha=0.5)
        axs[1, 1].set_title(f"{context_col.title()} Over Time")
        axs[1, 1].tick_params(axis="x", rotation=45)
    else:
        axs[1, 1].axis("off")

    plt.tight_layout()
    plt.show()
