import random
import numpy as np
import matplotlib.pyplot as plt
from user_profile import User
from bandit_linucb import LinUCB

def run_simulation(profile_type="default", strategy="random", nudge_types=None, max_steps=200):
    if nudge_types is None:
        nudge_types = ["notification", "email", "text", "real_time"]

    user = User(profile_type)
    engagement_history = []
    reward_history = []
    dropout_history = []
    dropout_step = None

    q_table = {}
    linucb_agent = LinUCB(n_actions=len(nudge_types)) if strategy == "linucb" else None

    for step in range(max_steps):
        state = user.get_state()

        # Strategy Logic
        if strategy == "random":
            nudge_type = random.choice(nudge_types)

        elif strategy == "epsilon_greedy":
            epsilon = 0.1
            state_key = tuple(sorted(state.items()))
            if random.random() < epsilon or state_key not in q_table:
                nudge_type = random.choice(nudge_types)
            else:
                q_values = q_table[state_key]
                nudge_type = max(q_values, key=q_values.get)

        elif strategy == "softmax":
            state_key = tuple(sorted(state.items()))
            if state_key not in q_table:
                q_table[state_key] = {nt: 0.0 for nt in nudge_types}
            q_values = np.array([q_table[state_key][nt] for nt in nudge_types])
            exp_q = np.exp(q_values - np.max(q_values))  # softmax stability
            probs = exp_q / np.sum(exp_q)
            nudge_type = np.random.choice(nudge_types, p=probs)

        elif strategy == "linucb":
            context = np.array([
                state["time"] / 24,
                state["energy"],
                state["stress"],
                user.fatigue,
                user.engagement
            ])
            action_index = linucb_agent.select_action(context)
            nudge_type = nudge_types[action_index]

        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

        # Nudge Response
        is_relevant = user.is_nudge_contextually_relevant(nudge_type, state)
        was_accepted = is_relevant and (random.random() > 0.2)
        user.receive_nudge(nudge_type, is_relevant, was_accepted)

        # Engagement + Reward Tracking
        reward = user.get_engagement_score()
        engagement_history.append(reward)
        reward_history.append(reward)

        # Dropout Probability Tracking
        dropout_prob = user.dropout_probability()
        dropout_history.append(dropout_prob)

        # Learning Update
        if strategy in ["epsilon_greedy", "softmax"]:
            if state_key not in q_table:
                q_table[state_key] = {nt: 0.0 for nt in nudge_types}
            alpha = 0.1
            q_table[state_key][nudge_type] += alpha * (reward - q_table[state_key][nudge_type])

        elif strategy == "linucb":
            linucb_agent.update(context, nudge_types.index(nudge_type), reward)

        if not user.is_active():
            dropout_step = step
            break

    return {
        "profile": profile_type,
        "strategy": strategy,
        "engagement": engagement_history,
        "reward": reward_history,
        "dropout_step": dropout_step or max_steps,
        "dropout_prob": dropout_history
    }

if __name__ == "__main__":
    profiles = ["default", "fitness_junkie", "night_owl", "burnout_prone", "distractible"]
    strategies = ["random", "epsilon_greedy", "softmax", "linucb"]
    max_steps = 200

    for profile in profiles:
        plt.figure(figsize=(12, 4))
        for strategy in strategies:
            result = run_simulation(profile_type=profile, strategy=strategy, max_steps=max_steps)
            plt.plot(result["dropout_prob"], label=strategy)
        plt.title(f"Dropout Probability Over Time – {profile}")
        plt.xlabel("Step")
        plt.ylabel("Dropout Probability")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
