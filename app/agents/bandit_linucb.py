import numpy as np
import pickle
import os

class LinUCB:
    def __init__(self, num_arms, context_dim, alpha=0.1):
        self.num_arms = num_arms
        self.context_dim = context_dim
        self.alpha = alpha

        # Initialize A and b for each arm
        self.A = [np.identity(context_dim) for _ in range(num_arms)]
        self.b = [np.zeros((context_dim, 1)) for _ in range(num_arms)]

    def select_action(self, context):
        context = context.reshape(-1, 1)  # ensure column vector
        p_values = []

        for arm in range(self.num_arms):
            A_inv = np.linalg.inv(self.A[arm])
            theta = A_inv @ self.b[arm]
            p = float((theta.T @ context) + self.alpha * np.sqrt(context.T @ A_inv @ context))
            p_values.append(p)

        return int(np.argmax(p_values))

    def update(self, arm, context, reward):
        context = context.reshape(-1, 1)
        self.A[arm] += context @ context.T
        self.b[arm] += reward * context

    def save(self, filepath="linucb_model.pkl"):
        with open(filepath, "wb") as f:
            pickle.dump({"A": self.A, "b": self.b}, f)

    def load(self, filepath="linucb_model.pkl"):
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                data = pickle.load(f)
                self.A = data["A"]
                self.b = data["b"]
