import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from nudge_logic import VISITS

def plot_strategy_comparison(results, title="Strategy Comparison", save_path="output/strategy_comparison.png"):
    x = np.arange(results[list(results.keys())[0]].shape[1])
    plt.figure(figsize=(10, 6))

    for label, data in results.items():
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        plt.plot(x, mean, label=f"{label} (mean)", linewidth=2)
        plt.fill_between(x, mean - std, mean + std, alpha=0.2)

    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Cumulative Reward")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Strategy comparison saved to: {save_path}")
    plt.show()

def plot_visit_heatmap(save_path="output/visit_heatmap.png"):
    rows = []
    for state_str, counts in VISITS.items():
        try:
            location = eval(state_str).get("location_type", "unknown")
        except:
            location = "unknown"
        for nudge, count in counts.items():
            rows.append({"location": location, "nudge_type": nudge, "count": count})
    df = pd.DataFrame(rows)
    if df.empty:
        print("No VISITS data available for heatmap.")
        return
    pivot = df.pivot_table(index="location", columns="nudge_type", values="count", aggfunc="sum").fillna(0)

    plt.figure(figsize=(8, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Oranges")
    plt.title("Visit Count Heatmap")
    plt.xlabel("Nudge Type")
    plt.ylabel("Location Context")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Visit heatmap saved to {save_path}")
    plt.show()

def plot_q_heatmap(save_path="output/q_heatmap.png"):
    from nudge_logic import Q_TABLE
    rows = []
    for state, nudges in Q_TABLE.items():
        try:
            location = eval(state).get("location_type", "unknown")
        except:
            location = "unknown"
        for nudge_type, q in nudges.items():
            rows.append({"location": location, "nudge_type": nudge_type, "Q_value": q})
    df = pd.DataFrame(rows)
    if df.empty:
        print("No Q-table data available.")
        return
    pivot = df.pivot_table(index="location", columns="nudge_type", values="Q_value", aggfunc="mean").fillna(0)

    plt.figure(figsize=(8, 4))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title("Q-Table Heatmap by Location")
    plt.xlabel("Nudge Type")
    plt.ylabel("Location Context")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Q heatmap saved to {save_path}")
    plt.show()

def plot_accuracy_regret_curves(logs, save_path="output/accuracy_regret.png"):
    plt.figure(figsize=(10, 5))
    for strategy, data in logs.items():
        regrets = np.cumsum(data["regrets"])
        accuracies = np.cumsum(data["accuracies"]) / (np.arange(len(data["accuracies"])) + 1)
        plt.plot(accuracies, regrets, label=strategy)

    plt.xlabel("Cumulative Accuracy")
    plt.ylabel("Cumulative Regret")
    plt.title("Regret vs. Accuracy")
    plt.legend()
    plt.grid(True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Regret vs. Accuracy plot saved to {save_path}")
    plt.show()

def plot_time_of_day_performance(logs, save_path="output/time_of_day_effects.png"):
    df = []
    for strategy, data in logs.items():
        times = pd.cut(data["times"], bins=[0, 6, 12, 18, 24], labels=["Night", "Morning", "Afternoon", "Evening"])
        df.extend([{"strategy": strategy, "time": t, "reward": r} for t, r in zip(times, data["rewards"])])

    df = pd.DataFrame(df)
    if df.empty:
        print("No reward data to analyze time-of-day effects.")
        return

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="time", y="reward", hue="strategy")
    plt.title("Cumulative Reward by Time of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Cumulative Reward")
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Time-of-day performance plot saved to {save_path}")
    plt.show()
