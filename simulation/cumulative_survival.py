import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

# Configuration
profile = "default"
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200

def collect_dropout_probabilities(profile, strategies, n_trials, max_steps):
    results = {s: [] for s in strategies}
    for strategy in strategies:
        print(f"Running: {strategy}")
        for _ in range(n_trials):
            sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
            probs = sim.get("dropout_prob", [])
            padded_probs = probs + [0.0] * (max_steps - len(probs))
            results[strategy].append(padded_probs)
    return results

def compute_survival_curves(prob_dict):
    survival_curves = {}
    for strategy, trials in prob_dict.items():
        survival = []
        for trial in trials:
            s = []
            prob = 1.0
            for p in trial:
                prob *= (1 - p)
                s.append(prob)
            survival.append(s)
        survival_curves[strategy] = np.array(survival)
    return survival_curves

def plot_survival(survival_curves, profile, max_steps):
    plt.figure(figsize=(12, 6))
    for strategy, curves in survival_curves.items():
        mean = np.mean(curves, axis=0)
        ci = 1.96 * np.std(curves, axis=0) / np.sqrt(curves.shape[0])
        plt.plot(mean, label=strategy)
        plt.fill_between(range(max_steps), mean - ci, mean + ci, alpha=0.2)
    plt.title(f"Cumulative Survival Curve – Profile: {profile}")
    plt.xlabel("Step")
    plt.ylabel("Survival Probability")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    filename = f"{profile}_cumulative_survival.png"
    plt.savefig(filename)
    print(f"Saved plot: {filename}")
    plt.show()

if __name__ == "__main__":
    probs = collect_dropout_probabilities(profile, strategies, n_trials, max_steps)
    curves = compute_survival_curves(probs)
    plot_survival(curves, profile, max_steps)
