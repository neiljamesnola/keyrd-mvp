import numpy as np

class LinUCB:
    def __init__(self, num_arms, context_dim=10, alpha=0.1):
        """
        LinUCB contextual bandit agent.

        Args:
            num_arms (int): Number of arms (actions).
            context_dim (int): Dimension of the context vector.
            alpha (float): Exploration-exploitation tradeoff parameter.
        """
        self.num_arms = num_arms
        self.context_dim = context_dim
        self.alpha = alpha

        # Per-arm covariance matrix A and reward vector b
        self.A = [np.identity(context_dim) for _ in range(num_arms)]
        self.b = [np.zeros((context_dim, 1)) for _ in range(num_arms)]

    def select_action(self, context):
        """
        Select the action with the highest UCB score.

        Args:
            context (np.ndarray): 1D array of contextual features.

        Returns:
            int: Index of the selected action.
        """
        context = context.reshape(-1, 1)
        p = np.zeros(self.num_arms)

        for a in range(self.num_arms):
            A_inv = np.linalg.inv(self.A[a])
            theta = A_inv @ self.b[a]
            uncertainty = self.alpha * np.sqrt(context.T @ A_inv @ context)
            p[a] = (theta.T @ context + uncertainty)[0, 0]

        return int(np.argmax(p))

    def update(self, context, arm, reward):
        """
        Update the parameters for the chosen arm.

        Args:
            context (np.ndarray): Context at the time of action.
            arm (int): Chosen action index.
            reward (float): Observed reward.
        """
        context = context.reshape(-1, 1)
        self.A[arm] += context @ context.T
        self.b[arm] += reward * context

    def get_theta(self, arm):
        """
        Return current weight estimate for the given arm.

        Args:
            arm (int): Action index.

        Returns:
            np.ndarray: Estimated coefficient vector.
        """
        A_inv = np.linalg.inv(self.A[arm])
        return A_inv @ self.b[arm]


class LinUCBAgent:
    def __init__(self, input_dim, output_dim, alpha=0.1):
        """
        Wrapper to conform LinUCB to the simulator API.

        Args:
            input_dim (int): Dimensionality of context vector.
            output_dim (int): Number of possible actions.
        """
        self.policy = LinUCB(num_arms=output_dim, context_dim=input_dim, alpha=alpha)

    def select_action(self, context):
        return self.policy.select_action(context)

    def store_transition(self, context, action, reward, next_state=None, done=None):
        self.policy.update(context, action, reward)

    def train(self):
        pass  # LinUCB is updated online in store_transition
