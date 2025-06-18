import sys
import os
sys.path.append(os.path.abspath("."))  # Make simulate.py importable

import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

# Configuration
profiles = ["default", "fitness_junkie", "stress_eater"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200
bin_width = 10  # Histogram bin size in steps

def collect_dropout_steps():
    dropout_data = {}
    for profile in profiles:
        print(f"\n📉 Dropout step collection for: {profile}")
        strat_steps = {}
        for strategy in strategies:
            print(f"  → {strategy}")
            steps = []
            for _ in range(n_trials):
                sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
                step = sim.get("dropout_step", max_steps)
                steps.append(step)
            strat_steps[strategy] = steps
        dropout_data[profile] = strat_steps
    return dropout_data

def plot_dropout_histograms(dropout_data):
    paths = []
    bins = np.arange(0, max_steps + bin_width, bin_width)

    for profile, strat_steps in dropout_data.items():
        plt.figure(figsize=(12, 6))
        for strategy, steps in strat_steps.items():
            plt.hist(steps, bins=bins, alpha=0.6, label=strategy, edgecolor='black')
        plt.title(f"Dropout Step Distribution – Profile: {profile}")
        plt.xlabel("Simulation Step")
        plt.ylabel("Number of Users Dropped")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        filename = f"{profile}_dropout_histogram.png"
        plt.savefig(filename)
        print(f"✅ Saved: {filename}")
        plt.close()
        paths.append(filename)
    return paths

if __name__ == "__main__":
    data = collect_dropout_steps()
    plot_dropout_histograms(data)
