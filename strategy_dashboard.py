import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation.simulate import run_simulation

strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200
profile = "fitness_junkie"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def evaluate_all_strategies(profile, strategies, max_steps, n_trials):
    results = {}

    for strat in strategies:
        engagement_trials = []
        reward_trials = []
        dropout_steps = []

        for i in range(n_trials):
            sim = run_simulation(profile_type=profile, strategy=strat, max_steps=max_steps)
            e = sim["engagement"] + [0.0] * (max_steps - len(sim["engagement"]))
            r = sim["reward"] + [0.0] * (max_steps - len(sim["reward"]))
            engagement_trials.append(e)
            reward_trials.append(r)
            dropout_steps.append(sim["dropout_step"])

        engagement_arr = np.array(engagement_trials)
        reward_arr = np.array(reward_trials)

        # Save to CSV
        df = pd.DataFrame({
            f"engagement_step_{i}": engagement_arr[:, i] for i in range(max_steps)
        })
        df["strategy"] = strat
        df["dropout_step"] = dropout_steps
        df.to_csv(f"{output_dir}/{profile}_{strat}_raw.csv", index=False)

        results[strat] = {
            "engagement": engagement_arr,
            "reward": reward_arr,
            "dropouts": np.array(dropout_steps)
        }

    return results

def ci95(data):
    mean = np.mean(data, axis=0)
    sem = np.std(data, axis=0) / np.sqrt(data.shape[0])
    return mean, 1.96 * sem

def plot_comparison_dashboard(results, profile):
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Avg Engagement Curve w/ CI
    for strat in strategies:
        mean, ci = ci95(results[strat]["engagement"])
        axs[0, 0].plot(mean, label=strat)
        axs[0, 0].fill_between(range(len(mean)), mean - ci, mean + ci, alpha=0.2)
    axs[0, 0].set_title(f"Engagement Over Time – {profile}")
    axs[0, 0].set_xlabel("Step")
    axs[0, 0].set_ylabel("Engagement Score")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Cumulative Reward w/ CI
    for strat in strategies:
        cum_rewards = results[strat]["reward"].sum(axis=1)
        mean = np.mean(cum_rewards)
        ci = 1.96 * np.std(cum_rewards) / np.sqrt(n_trials)
        axs[0, 1].bar(strat, mean, yerr=ci, capsize=5)
    axs[0, 1].set_title("Cumulative Reward by Strategy")
    axs[0, 1].set_ylabel("Reward")
    axs[0, 1].grid(True, axis='y')

    # 3. Survival Curve
    for strat in strategies:
        survival = []
        for t in range(max_steps):
            survivors = (results[strat]["dropouts"] > t).sum()
            survival.append(survivors / n_trials)
        axs[1, 0].plot(survival, label=strat)
    axs[1, 0].set_title("Survival Curve (Retention %)")
    axs[1, 0].set_xlabel("Step")
    axs[1, 0].set_ylabel("Active Users")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # 4. Dropout Histogram
    for strat in strategies:
        axs[1, 1].hist(results[strat]["dropouts"], bins=20, alpha=0.6, label=strat)
    axs[1, 1].set_title("Dropout Timing Distribution")
    axs[1, 1].set_xlabel("Step")
    axs[1, 1].set_ylabel("Users Dropped")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.suptitle(f"KeyRD Strategy Comparison Dashboard – Profile: {profile}", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig_path = f"{output_dir}/{profile}_dashboard.png"
    plt.savefig(fig_path, dpi=300)
    plt.show()
    print(f"✅ Dashboard saved to: {fig_path}")

if __name__ == "__main__":
    results = evaluate_all_strategies(profile, strategies, max_steps, n_trials)
    plot_comparison_dashboard(results, profile)
