import sys
import os
sys.path.append(os.path.abspath("."))  # Ensure simulate.py is accessible

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from simulate import run_simulation

# Configuration
profiles = ["default", "fitness_junkie", "stress_eater"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200
bin_size = 10  # For time-binning dropout risk

def collect_dropout_data():
    binned_data = {}
    n_bins = max_steps // bin_size

    for profile in profiles:
        print(f"\n🔍 Simulating: {profile}")
        profile_matrix = []

        for strategy in strategies:
            print(f"  → {strategy}")
            avg_bin_values = np.zeros(n_bins)

            for _ in range(n_trials):
                sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
                probs = sim.get("dropout_prob", []) + [0.0] * (max_steps - len(sim["dropout_prob"]))
                bins = [np.mean(probs[i:i+bin_size]) for i in range(0, max_steps, bin_size)]
                avg_bin_values += np.array(bins)

            avg_bin_values /= n_trials
            profile_matrix.append(avg_bin_values)

        binned_data[profile] = np.array(profile_matrix)  # shape: [strategies x bins]

    return binned_data

def plot_heatmaps(binned_data):
    paths = []
    for profile, matrix in binned_data.items():
        plt.figure(figsize=(12, 5))

        sns.heatmap(
            matrix,
            cmap="YlOrRd",
            xticklabels=[f"{i*bin_size}-{(i+1)*bin_size}" for i in range(matrix.shape[1])],
            yticklabels=strategies,
            annot=True,
            fmt=".4f"
            # norm=LogNorm()  # optional for visual contrast on small values
        )

        plt.title(f"Dropout Probability Heatmap – Profile: {profile}")
        plt.xlabel("Step Window")
        plt.ylabel("Strategy")
        plt.tight_layout()

        filename = f"{profile}_dropout_heatmap.png"
        plt.savefig(filename)
        print(f"✅ Saved: {filename}")
        plt.close()
        paths.append(filename)
    return paths

if __name__ == "__main__":
    data = collect_dropout_data()
    plot_heatmaps(data)
