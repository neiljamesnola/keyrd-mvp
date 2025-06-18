import os
import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

profiles = ["default", "fitness_junkie", "night_owl", "burnout_prone", "distractible"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200

def ci95(data):
    mean = np.mean(data, axis=0)
    sem = np.std(data, axis=0) / np.sqrt(data.shape[0])
    return mean, 1.96 * sem

def evaluate(profile, strategy):
    engagement_trials = []
    reward_trials = []
    dropout_trials = []
    dropout_probs = []

    for _ in range(n_trials):
        result = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
        pad = lambda seq: seq + [0.0] * (max_steps - len(seq))
        engagement_trials.append(pad(result["engagement"]))
        reward_trials.append(pad(result["reward"]))
        dropout_probs.append(pad(result["dropout_prob"]))
        dropout_trials.append(result["dropout_step"])

    return {
        "engagement": np.array(engagement_trials),
        "reward": np.array(reward_trials),
        "dropout_probs": np.array(dropout_probs),
        "dropouts": np.array(dropout_trials)
    }

def plot_profile_dashboard(profile, results):
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    # Engagement
    for strat in strategies:
        mean, ci = ci95(results[strat]["engagement"])
        axs[0, 0].plot(mean, label=strat)
        axs[0, 0].fill_between(range(max_steps), mean - ci, mean + ci, alpha=0.2)
    axs[0, 0].set_title("Engagement Over Time")
    axs[0, 0].set_ylabel("Engagement")
    axs[0, 0].set_xlabel("Step")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Reward
    for strat in strategies:
        cum = results[strat]["reward"].sum(axis=1)
        mean = np.mean(cum)
        ci = 1.96 * np.std(cum) / np.sqrt(n_trials)
        axs[0, 1].bar(strat, mean, yerr=ci, capsize=5)
    axs[0, 1].set_title("Cumulative Reward")
    axs[0, 1].set_ylabel("Total Reward")
    axs[0, 1].grid(True, axis='y')

    # Survival
    for strat in strategies:
        survival = [
            (results[strat]["dropouts"] > t).sum() / n_trials
            for t in range(max_steps)
        ]
        axs[1, 0].plot(survival, label=strat)
    axs[1, 0].set_title("Survival Curve (1 - Dropout)")
    axs[1, 0].set_xlabel("Step")
    axs[1, 0].set_ylabel("Proportion Active")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Dropout Probability
    for strat in strategies:
        mean = results[strat]["dropout_probs"].mean(axis=0)
        axs[1, 1].plot(mean, label=strat)
    axs[1, 1].set_title("Avg Dropout Probability Over Time")
    axs[1, 1].set_xlabel("Step")
    axs[1, 1].set_ylabel("Probability")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.suptitle(f"Strategy Comparison – Profile: {profile}", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    for profile in profiles:
        print(f"⏳ Running simulations for profile: {profile}")
        results = {strat: evaluate(profile, strat) for strat in strategies}
        plot_profile_dashboard(profile, results)
