import numpy as np
from bandit_linucb import LinUCB

def test_linucb_basic():
    np.random.seed(42)

    agent = LinUCB(n_actions=3, d=2, alpha=0.1)

    context = np.array([0.5, 0.2])  # example context

    # Before update, all arms should be equal → pick any
    action = agent.select_action(context)
    assert 0 <= action < 3, "Action should be valid index"

    # Update arm 0 with a positive reward
    agent.update(context, a=0, reward=1.0)

    # After update, arm 0 should have higher preference
    action = agent.select_action(context)
    print(f"Chosen action after update: {action}")
    assert action == 0, "Should prefer updated arm"

if __name__ == "__main__":
    test_linucb_basic()
    print("✅ LinUCB unit test passed.")
