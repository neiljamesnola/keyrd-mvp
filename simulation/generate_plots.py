import os
import numpy as np
import pandas as pd
from viz import (
    plot_engagement,
    plot_reward_distributions,
    plot_dropout_heatmap,
    plot_survival_curves,
    plot_engagement_gradient,
    plot_reward_velocity,
    plot_reward_diversity,
    plot_action_entropy_over_time,
    plot_action_dynamics
)

def load_agent_data(profile_dir):
    results = {}
    for fname in os.listdir(profile_dir):
        if fname.endswith("_reward.csv"):
            agent_key = fname.replace("_reward.csv", "")
            print(f"[DEBUG] Loading agent: {agent_key}")

            try:
                reward_df = pd.read_csv(os.path.join(profile_dir, f"{agent_key}_reward.csv"))
                engagement_df = pd.read_csv(os.path.join(profile_dir, f"{agent_key}_engagement.csv"))
                dropout_df = pd.read_csv(os.path.join(profile_dir, f"{agent_key}_dropout.csv"))
            except FileNotFoundError as e:
                print(f"[WARNING] Missing file for agent {agent_key}: {e}")
                continue

            # Reshape reward data
            reward_long = reward_df.melt(ignore_index=False).dropna()
            reward_long = reward_long.rename(columns={"value": "reward"})
            reward_long["timestep"] = reward_long["variable"].str.extract("t(\d+)").astype(int)
            reward_long["run"] = reward_long.index
            reward_long = reward_long[["run", "timestep", "reward"]]

            # Reshape engagement data
            engagement_long = engagement_df.melt(ignore_index=False).dropna()
            engagement_long = engagement_long.rename(columns={"value": "engagement"})
            engagement_long["timestep"] = engagement_long["variable"].str.extract("t(\d+)").astype(int)
            engagement_long["run"] = engagement_long.index
            engagement_long = engagement_long[["run", "timestep", "engagement"]]

            # Merge reward and engagement
            df = pd.merge(reward_long, engagement_long, on=["run", "timestep"], how="outer")

            # Add dropout info
            dropout_map = dropout_df["dropout_step"].to_dict()
            df["dropout"] = df["run"].map(dropout_map)

            df["agent"] = agent_key
            results[agent_key] = df
    return results

def main():
    profiles = ["resilient", "stress_eater", "fatigue_sensitive"]
    for profile in profiles:
        print(f"📊 Generating plots for profile: {profile}")
        profile_dir = os.path.join("results", profile)
        if not os.path.isdir(profile_dir):
            print(f"[WARNING] Skipping missing profile directory: {profile_dir}")
            continue

        results = load_agent_data(profile_dir)

        # Call all visualizations
        plot_engagement(results, profile)
        plot_reward_distributions(results, profile)
        plot_dropout_heatmap(results, profile)
        plot_survival_curves(results, profile)
        plot_engagement_gradient(results, profile)
        plot_reward_velocity(results, profile)
        plot_reward_diversity(results, profile)
        plot_action_entropy_over_time(results, profile)
        plot_action_dynamics(results, profile)

if __name__ == "__main__":
    main()
