import sys
import os
sys.path.append(os.path.abspath("."))  # Ensure simulate.py is visible

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from simulate import run_simulation

# Configuration
profiles = ["default", "fitness_junkie", "stress_eater"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200

def collect_outcome_data():
    results = []
    for profile in profiles:
        print(f"\n🎯 Collecting outcomes for: {profile}")
        for strategy in strategies:
            print(f"  → {strategy}")
            for _ in range(n_trials):
                sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
                final_reward = np.sum(sim.get("reward", []))
                final_engagement = sim.get("engagement", [-1])[-1]
                dropout_step = sim.get("dropout_step", max_steps)
                results.append({
                    "profile": profile,
                    "strategy": strategy,
                    "reward": final_reward,
                    "engagement": final_engagement,
                    "dropout": dropout_step
                })
    return results

def plot_violin_and_boxplots(data):
    df = pd.DataFrame(data)
    output_paths = []

    for metric in ["reward", "engagement", "dropout"]:
        for profile in profiles:
            plt.figure(figsize=(10, 6))
            subset = df[df["profile"] == profile]
            sns.violinplot(x="strategy", y=metric, data=subset, inner=None, color=".9")
            sns.boxplot(x="strategy", y=metric, data=subset, width=0.3)
            plt.title(f"{metric.title()} Distribution – Profile: {profile}")
            plt.ylabel(metric.title())
            plt.xlabel("Strategy")
            plt.grid(True)
            plt.tight_layout()

            filename = f"{profile}_{metric}_distribution.png"
            plt.savefig(filename)
            print(f"✅ Saved: {filename}")
            plt.close()
            output_paths.append(filename)

    return output_paths

if __name__ == "__main__":
    data = collect_outcome_data()
    plot_violin_and_boxplots(data)
