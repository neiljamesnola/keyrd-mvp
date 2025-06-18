import numpy as np
import matplotlib.pyplot as plt
from bandit_linucb import LinUCB

def run_linucb_demo(n_actions=4, d=5, steps=200, alpha=0.2):
    agent = LinUCB(n_actions=n_actions, d=d, alpha=alpha)
    
    action_counts = np.zeros(n_actions)
    cumulative_rewards = np.zeros(n_actions)
    reward_history = []
    action_history = []
    uncertainty_history = [[] for _ in range(n_actions)]
    score_history = []

    for t in range(steps):
        context = np.random.rand(d)  # Simulated random context
        scores = agent.score_all_actions(context)
        action = np.argmax(scores)
        uncertainty = [s - agent.get_theta(a).T @ context.reshape(-1, 1) for a, s in enumerate(scores)]

        # Simulated reward function (e.g., arm 1 is best)
        reward = 1.0 if action == 1 else 0.3 + 0.2 * np.random.randn()
        reward = max(0.0, min(1.0, reward))  # clip to [0, 1]

        agent.update(context, action, reward)

        action_counts[action] += 1
        cumulative_rewards[action] += reward
        reward_history.append(reward)
        action_history.append(action)
        score_history.append(scores)

        for a in range(n_actions):
            uncertainty_history[a].append(float(uncertainty[a]))

    return {
        "action_counts": action_counts,
        "cumulative_rewards": cumulative_rewards,
        "reward_history": reward_history,
        "action_history": action_history,
        "uncertainty_history": uncertainty_history,
        "score_history": np.array(score_history)
    }

def plot_linucb_dashboard(results, n_actions=4):
    steps = len(results["reward_history"])
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Action distribution
    axs[0, 0].bar(range(n_actions), results["action_counts"])
    axs[0, 0].set_title("Action Selection Counts")
    axs[0, 0].set_xlabel("Action")
    axs[0, 0].set_ylabel("Count")
    axs[0, 0].grid(True)

    # 2. Cumulative rewards
    axs[0, 1].bar(range(n_actions), results["cumulative_rewards"])
    axs[0, 1].set_title("Cumulative Reward per Action")
    axs[0, 1].set_xlabel("Action")
    axs[0, 1].set_ylabel("Reward")
    axs[0, 1].grid(True)

    # 3. UCB scores over time
    for a in range(n_actions):
        axs[1, 0].plot(results["score_history"][:, a], label=f"Action {a}")
    axs[1, 0].set_title("UCB Score Evolution")
    axs[1, 0].set_xlabel("Step")
    axs[1, 0].set_ylabel("UCB Score")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # 4. Uncertainty over time
    for a in range(n_actions):
        axs[1, 1].plot(results["uncertainty_history"][a], label=f"Action {a}")
    axs[1, 1].set_title("Estimated Uncertainty by Action")
    axs[1, 1].set_xlabel("Step")
    axs[1, 1].set_ylabel("Uncertainty")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    results = run_linucb_demo(n_actions=4, d=5, steps=200, alpha=0.25)
    plot_linucb_dashboard(results)
