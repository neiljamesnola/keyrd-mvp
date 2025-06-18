import sys
import os
sys.path.append(os.path.abspath("."))  # Ensure simulate.py is visible

import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

# Configuration
profiles = ["default", "fitness_junkie", "stress_eater"]
strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
n_trials = 20
max_steps = 200
smoothing = 3  # optional moving average window

def collect_reward_velocities():
    velocities = {}
    for profile in profiles:
        print(f"\n⚡ Reward velocity for: {profile}")
        strat_vel = {}
        for strategy in strategies:
            print(f"  → {strategy}")
            all_vels = []

            for _ in range(n_trials):
                sim = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
                rewards = sim.get("reward", [])
                if not rewards:
                    rewards = [0.0] * max_steps
                padded = rewards + [rewards[-1]] * (max_steps - len(rewards))
                delta = np.gradient(padded)

                if smoothing > 1:
                    kernel = np.ones(smoothing) / smoothing
                    delta = np.convolve(delta, kernel, mode='same')

                all_vels.append(delta)

            strat_vel[strategy] = np.mean(all_vels, axis=0)
        velocities[profile] = strat_vel
    return velocities

def plot_reward_velocity_curves(velocities):
    paths = []
    for profile, strat_curves in velocities.items():
        plt.figure(figsize=(12, 6))
        for strategy, vel_curve in strat_curves.items():
            plt.plot(vel_curve, label=strategy)
        plt.axhline(0, color='gray', linestyle='--')
        plt.title(f"Reward Velocity Curve – Profile: {profile}")
        plt.xlabel("Step")
        plt.ylabel("Δ Reward / Step")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        filename = f"{profile}_reward_velocity_curve.png"
        plt.savefig(filename)
        print(f"✅ Saved: {filename}")
        plt.close()
        paths.append(filename)
    return paths

if __name__ == "__main__":
    velocity_data = collect_reward_velocities()
    plot_reward_velocity_curves(velocity_data)
