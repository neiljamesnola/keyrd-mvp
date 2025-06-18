import os
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from itertools import combinations

# --------------------
# CONFIGURATION
# --------------------
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "analysis")
USER_TYPES = ["resilient", "stress_eater", "fatigue_sensitive"]
METRICS = ["reward", "engagement"]
ALPHA = 0.05

summary_stats = []
pairwise_tests = []
harmonic_means = []

# --------------------
# MAIN ANALYSIS LOOP
# --------------------
for user_type in USER_TYPES:
    user_path = os.path.join(RESULTS_DIR, user_type)
    if not os.path.exists(user_path):
        print(f" Missing directory for: {user_type}")
        continue

    agent_files = [f for f in os.listdir(user_path) if f.endswith(".csv")]
    agents = [f.replace(".csv", "") for f in agent_files]
    agent_data = {agent: pd.read_csv(os.path.join(user_path, f"{agent}.csv")) for agent in agents}

    for metric in METRICS:
        means = {}
        stds = {}
        ns = {}

        for agent, df in agent_data.items():
            vals = df[metric].dropna()
            mean = vals.mean()
            std = vals.std()
            n = len(vals)

            summary_stats.append({
                "user_type": user_type,
                "agent": agent,
                "metric": metric,
                "mean": mean,
                "std": std,
                "n": n
            })

            means[agent] = mean
            stds[agent] = std
            ns[agent] = n

        # Pairwise t-tests
        for agent1, agent2 in combinations(agents, 2):
            vals1 = agent_data[agent1][metric].dropna()
            vals2 = agent_data[agent2][metric].dropna()
            t_stat, p_val = ttest_ind(vals1, vals2, equal_var=False)
            pairwise_tests.append({
                "user_type": user_type,
                "metric": metric,
                "agent_1": agent1,
                "agent_2": agent2,
                "t_stat": t_stat,
                "p_value": p_val,
                "significant": p_val < ALPHA
            })

        # Harmonic mean scores (lower std, higher mean = better)
        for agent in agents:
            mean = means.get(agent, np.nan)
            std = stds.get(agent, np.nan)
            if mean > 0 and std > 0:
                h_score = 2 * (mean * (1 / std)) / (mean + (1 / std))
            else:
                h_score = np.nan

            harmonic_means.append({
                "user_type": user_type,
                "agent": agent,
                "metric": metric,
                "harmonic_mean_score": h_score
            })

# --------------------
# OUTPUT
# --------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

pd.DataFrame(summary_stats).to_csv(os.path.join(OUTPUT_DIR, "summary_statistics.csv"), index=False)
pd.DataFrame(pairwise_tests).to_csv(os.path.join(OUTPUT_DIR, "pairwise_ttests.csv"), index=False)
pd.DataFrame(harmonic_means).to_csv(os.path.join(OUTPUT_DIR, "harmonic_means.csv"), index=False)

print("\n Analysis complete. Files saved to 'analysis' directory:")
print(" - summary_statistics.csv")
print(" - pairwise_ttests.csv")
print(" - harmonic_means.csv")
