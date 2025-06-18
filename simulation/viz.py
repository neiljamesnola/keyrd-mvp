import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import entropy

sns.set(style="whitegrid")


def _ensure_df(df_like):
    if isinstance(df_like, pd.DataFrame):
        return df_like
    raise TypeError(f"Expected DataFrame, got {type(df_like)}")


def plot_engagement(results, profile):
    plt.figure(figsize=(12, 6))
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        if "engagement" not in df.columns or "timestep" not in df.columns:
            continue
        sns.lineplot(
            data=df.dropna(subset=["engagement"]),
            x="timestep",
            y="engagement",
            label=agent_name,
            alpha=0.3,
            linewidth=1
        )
    plt.title(f"{profile} – Engagement Trajectories")
    plt.xlabel("Timestep")
    plt.ylabel("Engagement Level")
    plt.legend(title="Agent", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_engagement.png")
    plt.close()


def plot_reward_distributions(results, profile):
    plt.figure(figsize=(12, 6))
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        print(f"[DEBUG] Agent: {agent_name}, Columns: {df.columns.tolist()}")
        rewards = df["reward"].dropna()
        if len(rewards) > 1 and rewards.var() > 1e-5:
            sns.kdeplot(rewards, label=agent_name, fill=True, alpha=0.3)
    plt.title(f"{profile} – Reward Distributions")
    plt.xlabel("Reward")
    plt.ylabel("Density")
    plt.legend(title="Agent")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_reward_distribution.png")
    plt.close()


def plot_dropout_heatmap(results, profile, max_t=200):
    agent_names = list(results.keys())
    matrix = np.zeros((len(agent_names), max_t))
    for i, agent_name in enumerate(agent_names):
        df = _ensure_df(results[agent_name])
        dropouts = df.dropna(subset=["dropout"]).drop_duplicates(subset=["run"])["dropout"].astype(int)
        for step in dropouts:
            if 0 <= step < max_t:
                matrix[i, step] += 1
    plt.figure(figsize=(14, 5))
    sns.heatmap(matrix, cmap="Reds", cbar=True, xticklabels=20, yticklabels=agent_names)
    plt.title(f"{profile} – Dropout Timing Heatmap")
    plt.xlabel("Timestep")
    plt.ylabel("Agent")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_dropout_heatmap.png")
    plt.close()


def plot_survival_curves(results, profile, max_t=200):
    plt.figure(figsize=(12, 6))
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        print(f"[DEBUG] Columns in {agent_name} DataFrame: {df.columns.tolist()}")  # ✅ correct position

        n_runs = df["run"].nunique()
        survival = np.ones(max_t)
        dropouts = df.dropna(subset=["dropout"]).drop_duplicates(subset=["run"])["dropout"].astype(int)
        for step in dropouts:
            if step < max_t:
                survival[step:] -= 1 / n_runs
        plt.plot(survival, label=agent_name)

    plt.title(f"{profile} – Survival Curves")
    plt.xlabel("Timestep")
    plt.ylabel("Survival Probability")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/{profile}_survival_curve.png")
    plt.close()


def plot_engagement_gradient(results, profile):
    plt.figure(figsize=(12, 6))
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        for run_id in df["run"].unique():
            run_data = df[df["run"] == run_id]["engagement"].dropna()
            if len(run_data) > 1:
                gradient = np.gradient(run_data)
                plt.plot(gradient, label=agent_name, alpha=0.2)
    plt.title(f"{profile} – Engagement Gradient")
    plt.xlabel("Timestep")
    plt.ylabel("Δ Engagement")
    plt.legend(title="Agent", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_engagement_gradient.png")
    plt.close()


def plot_reward_velocity(results, profile):
    plt.figure(figsize=(12, 6))
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        for run_id in df["run"].unique():
            run_rewards = df[df["run"] == run_id]["reward"].dropna()
            if len(run_rewards) > 1:
                velocity = np.diff(run_rewards)
                plt.plot(velocity, label=agent_name, alpha=0.2)
    plt.title(f"{profile} – Reward Velocity")
    plt.xlabel("Timestep")
    plt.ylabel("Reward Δ per Step")
    plt.legend(title="Agent", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_reward_velocity.png")
    plt.close()


def plot_reward_diversity(results, profile):
    data = []
    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        for run_id in df["run"].unique():
            run_rewards = df[df["run"] == run_id]["reward"].dropna()
            if len(run_rewards):
                data.append({"Agent": agent_name, "MeanReward": np.mean(run_rewards)})
    df_summary = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df_summary, x="Agent", y="MeanReward")
    plt.title(f"{profile} – Reward Distribution Diversity")
    plt.tight_layout()
    plt.savefig(f"results/{profile}_reward_violin.png")
    plt.close()


def plot_action_entropy_over_time(results, profile, n_actions=None):
    entropy_data = {}

    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        if "action" not in df.columns:
            continue

        pivot = df.pivot(index="run", columns="timestep", values="action")
        agent_entropy = []

        for t in sorted(pivot.columns):
            actions_t = pivot[t].dropna().astype(int)
            counts = actions_t.value_counts().sort_index()
            action_probs = np.zeros(n_actions or counts.index.max() + 1)
            total = counts.sum()
            for a, count in counts.items():
                action_probs[a] = count / total
            agent_entropy.append(entropy(action_probs, base=2))

        entropy_data[agent_name] = agent_entropy

    plt.figure(figsize=(12, 6))
    for agent_name, ent in entropy_data.items():
        plt.plot(ent, label=agent_name)
    plt.title(f"{profile} – Action Entropy Over Time")
    plt.xlabel("Timestep")
    plt.ylabel("Entropy (bits)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/{profile}_action_entropy.png")
    plt.close()


def plot_action_dynamics(results, profile, n_actions=None):
    all_action_counts = []
    all_action_timesteps = []

    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        if "action" not in df.columns:
            continue

        action_counts = df["action"].value_counts().sort_index()
        max_action_id = int(action_counts.index.max())
        action_freq = np.zeros(n_actions or max_action_id + 1)
        for a, count in action_counts.items():
            action_freq[int(a)] = count
        all_action_counts.append((agent_name, action_freq))

        pivot = df.pivot(index="run", columns="timestep", values="action")
        for t in pivot.columns:
            counts = pivot[t].value_counts().sort_index()
            freq = np.zeros(n_actions or int(counts.index.max()) + 1)
            for a, count in counts.items():
                freq[int(a)] = count
            all_action_timesteps.append((agent_name, t, freq))

    plt.figure(figsize=(12, 6))
    for agent_name, freqs in all_action_counts:
        plt.plot(range(len(freqs)), freqs, label=agent_name)
    plt.title(f"{profile} – Total Action Frequencies")
    plt.xlabel("Action ID")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/{profile}_action_frequency.png")
    plt.close()

    for agent_name in set(name for name, _, _ in all_action_timesteps):
        agent_data = [(t, f) for name, t, f in all_action_timesteps if name == agent_name]
        agent_data.sort(key=lambda x: x[0])
        matrix = np.stack([f for _, f in agent_data], axis=1)

        plt.figure(figsize=(14, 5))
        sns.heatmap(matrix, cmap="Blues", cbar=True)
        plt.title(f"{profile} – Action Dynamics Over Time ({agent_name})")
        plt.xlabel("Timestep")
        plt.ylabel("Action ID")
        plt.tight_layout()
        fname = f"{profile}_{agent_name.lower().replace(' ', '_')}_action_dynamics.png"
        plt.savefig(f"results/{fname}")
        plt.close()


def export_summary_stats(results, profile, output_dir="results"):
    summary_dir = os.path.join(output_dir, "summaries", profile)
    os.makedirs(summary_dir, exist_ok=True)
    rows = []

    for agent_name, df_like in results.items():
        df = _ensure_df(df_like)
        grouped = df.groupby("run")
        rewards = grouped["reward"].mean().dropna()
        engagements = grouped["engagement"].mean().dropna()

        rows.append([
            agent_name,
            rewards.mean() if not rewards.empty else np.nan,
            rewards.std() if not rewards.empty else np.nan,
            engagements.mean() if not engagements.empty else np.nan,
            engagements.std() if not engagements.empty else np.nan
        ])

    summary_df = pd.DataFrame(
        rows,
        columns=["Agent", "MeanReward", "StdReward", "MeanEngagement", "StdEngagement"]
    )
    summary_df.to_csv(os.path.join(summary_dir, f"{profile}_summary.csv"), index=False)