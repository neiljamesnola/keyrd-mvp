import os
import pickle
import numpy as np

class LinUCB:
    def __init__(self, num_arms: int, context_dim: int = 5, alpha: float = 0.1):
        self.num_arms = num_arms
        self.context_dim = context_dim
        self.alpha = alpha

        print(f"[LinUCB INIT] num_arms={num_arms}, context_dim={context_dim}, alpha={alpha}")

        self.A = [np.identity(context_dim) for _ in range(num_arms)]
        self.b = [np.zeros((context_dim, 1)) for _ in range(num_arms)]


    def select_action(self, context_vector):
        if context_vector.shape[0] != self.context_dim:
            raise ValueError(
                f"[LinUCB Error] Context vector shape mismatch: expected {self.context_dim}, got {context_vector.shape[0]}"
            )

        context = context_vector.reshape(-1, 1)
        p_values = []

        for a in range(self.num_arms):
            A_inv = np.linalg.inv(self.A[a])
            theta = A_inv @ self.b[a]
            p = (theta.T @ context)[0, 0] + self.alpha * np.sqrt(context.T @ A_inv @ context)[0, 0]
            p_values.append(p)

        return int(np.argmax(p_values))

    def update(self, chosen_arm, reward, context_vector):
        if context_vector.shape[0] != self.context_dim:
            raise ValueError(
                f"[LinUCB Error] Context vector shape mismatch during update: expected {self.context_dim}, got {context_vector.shape[0]}"
            )

        context = context_vector.reshape(-1, 1)
        self.A[chosen_arm] += context @ context.T
        self.b[chosen_arm] += reward * context

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump({
                'A': self.A,
                'b': self.b,
                'num_arms': self.num_arms,
                'context_dim': self.context_dim,
                'alpha': self.alpha
            }, f)

    def load(self, filepath):
        with open(filepath, "rb") as f:
            state = pickle.load(f)
            self.A = state['A']
            self.b = state['b']
            self.num_arms = state['num_arms']
            self.context_dim = state['context_dim']
            self.alpha = state['alpha']

def load_model_or_initialize(num_arms=5, context_dim=26, alpha=0.1, filepath="instance/linucb_model.pkl"):
    model = LinUCB(num_arms, context_dim, alpha)
    if os.path.exists(filepath):
        try:
            model.load(filepath)
            print(f"✅ Loaded LinUCB model from {filepath}")
        except Exception as e:
            print(f"⚠️ Failed to load LinUCB model: {e} — reinitializing")
    else:
        print("📦 No existing model found — initializing new LinUCB agent")
    return model
