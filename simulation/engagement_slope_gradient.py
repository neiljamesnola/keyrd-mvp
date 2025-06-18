import sys
import os
sys.path.append(os.path.abspath("."))  # Make sure simulate.py is importable

import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

# Configuration
profiles = ["default", "fitness_junkie", "stress_eater"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200
smoothing = 3  # Optional: moving average window size for slope smoothing

def collect_engagement_slopes():
    slopes = {}
    for profile in profiles:
        print(f"\n📈 Calculating slope curves for: {profile}")
        strat_slopes = {}
        for strategy in strategies:
            print(f"  → {strategy}")
            all_slopes = []

            for _ in range(n_trials):
                sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
                engagement = sim.get("engagement", [])
                if not engagement:
                    engagement = [0.0] * max_steps
                padded = engagement + [engagement[-1]] * (max_steps - len(engagement))
                gradient = np.gradient(padded)

                if smoothing > 1:
                    kernel = np.ones(smoothing) / smoothing
                    gradient = np.convolve(gradient, kernel, mode='same')

                all_slopes.append(gradient)

            strat_slopes[strategy] = np.mean(all_slopes, axis=0)
        slopes[profile] = strat_slopes
    return slopes

def plot_slope_gradients(slopes):
    paths = []
    for profile, strat_curves in slopes.items():
        plt.figure(figsize=(12, 6))
        for strategy, slope_curve in strat_curves.items():
            plt.plot(slope_curve, label=strategy)
        plt.axhline(0, color='gray', linestyle='--', linewidth=1)
        plt.title(f"Engagement Slope Gradient – Profile: {profile}")
        plt.xlabel("Step")
        plt.ylabel("d(Engagement)/dt")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        filename = f"{profile}_engagement_slope_gradient.png"
        plt.savefig(filename)
        print(f"✅ Saved: {filename}")
        plt.close()
        paths.append(filename)
    return paths

if __name__ == "__main__":
    slopes = collect_engagement_slopes()
    plot_slope_gradients(slopes)
