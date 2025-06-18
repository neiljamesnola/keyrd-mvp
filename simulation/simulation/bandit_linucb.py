import numpy as np
from collections import defaultdict

class LinUCB:
    def __init__(self, n_features, alpha=0.3, actions=None):
        self.alpha = alpha
        self.actions = actions if actions else []
        self.n_features = n_features
        self.A = {a: np.identity(n_features) for a in self.actions}
        self.b = {a: np.zeros((n_features, 1)) for a in self.actions}

    def add_action(self, action):
        if action not in self.A:
            self.A[action] = np.identity(self.n_features)
            self.b[action] = np.zeros((self.n_features, 1))
            self.actions.append(action)

    def select_action(self, context_vector):
        x = context_vector.reshape(-1, 1)
        scores = {}
        for a in self.actions:
            A_inv = np.linalg.inv(self.A[a])
            theta = A_inv @ self.b[a]
            p = float(theta.T @ x + self.alpha * np.sqrt(x.T @ A_inv @ x))
            scores[a] = p
        return max(scores, key=scores.get)

    def update(self, action, context_vector, reward):
        x = context_vector.reshape(-1, 1)
        self.A[action] += x @ x.T
        self.b[action] += reward * x
