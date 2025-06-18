import numpy as np
from collections import defaultdict

class BanditStrategy:
    def __init__(self, actions):
        self.actions = actions
        self.action_counts = defaultdict(int)
        self.q_values = defaultdict(float)
        self.total_count = 0

    def select_action(self, state):
        raise NotImplementedError

    def update(self, action, reward, state=None):
        self.total_count += 1
        self.action_counts[action] += 1
        alpha = 1 / self.action_counts[action]
        self.q_values[action] += alpha * (reward - self.q_values[action])


class RandomStrategy(BanditStrategy):
    def select_action(self, state):
        return np.random.choice(self.actions)


class EpsilonGreedyStrategy(BanditStrategy):
    def __init__(self, actions, epsilon=0.1):
        super().__init__(actions)
        self.epsilon = epsilon

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        return max(self.actions, key=lambda a: self.q_values[a])


class SoftmaxStrategy(BanditStrategy):
    def __init__(self, actions, tau=1.0):
        super().__init__(actions)
        self.tau = tau

    def select_action(self, state):
        q_vals = np.array([self.q_values[a] for a in self.actions])
        exp_q = np.exp(q_vals / self.tau)
        probs = exp_q / np.sum(exp_q)
        return np.random.choice(self.actions, p=probs)


class ThompsonSamplingStrategy(BanditStrategy):
    def __init__(self, actions):
        super().__init__(actions)
        self.successes = defaultdict(lambda: 1)
        self.failures = defaultdict(lambda: 1)

    def select_action(self, state):
        samples = {a: np.random.beta(self.successes[a], self.failures[a]) for a in self.actions}
        return max(samples, key=samples.get)

    def update(self, action, reward, state=None):
        if reward > 0:
            self.successes[action] += 1
        else:
            self.failures[action] += 1


class LinUCBStrategy:
    def __init__(self, actions, d=5, alpha=1.0):
        self.actions = actions
        self.alpha = alpha
        self.d = d
        self.A = {a: np.identity(d) for a in actions}
        self.b = {a: np.zeros((d,)) for a in actions}

    def select_action(self, state_vec):
        p = {}
        for a in self.actions:
            A_inv = np.linalg.inv(self.A[a])
            theta = A_inv @ self.b[a]
            p[a] = theta @ state_vec + self.alpha * np.sqrt(state_vec.T @ A_inv @ state_vec)
        return max(p, key=p.get)

    def update(self, action, reward, state_vec):
        self.A[action] += np.outer(state_vec, state_vec)
        self.b[action] += reward * state_vec
