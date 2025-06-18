import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

# Shared MLP model with dropout
class MLP(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)

# Bootstrapped DQN with multiple heads
class BootstrappedDQNAgent:
    def __init__(self, input_dim, output_dim, hidden_dim=64, lr=1e-3, n_heads=10, gamma=0.99):
        self.output_dim = output_dim
        self.n_heads = n_heads
        self.gamma = gamma
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.models = [MLP(input_dim, output_dim, hidden_dim).to(self.device) for _ in range(n_heads)]
        self.optimizers = [optim.Adam(model.parameters(), lr=lr) for model in self.models]
        self.buffer = []
        self.batch_size = 32
        self.max_buffer_size = 10000

    def select_action(self, context):
        context_tensor = torch.tensor(context, dtype=torch.float32, device=self.device).unsqueeze(0)
        model = random.choice(self.models)
        with torch.no_grad():
            q_values = model(context_tensor)
        return int(torch.argmax(q_values).item())

    def store_transition(self, context, action, reward, next_state=None, done=None):
        if len(self.buffer) >= self.max_buffer_size:
            self.buffer.pop(0)
        self.buffer.append((context, action, reward))

    def train(self):
        if len(self.buffer) < self.batch_size:
            return

        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards = zip(*batch)
        states = torch.tensor(np.stack(states), dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.int64, device=self.device).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device).unsqueeze(1)

        for model, optimizer in zip(self.models, self.optimizers):
            q_vals = model(states).gather(1, actions)
            loss = nn.MSELoss()(q_vals, rewards)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

# Neural Thompson Sampling agent with MC Dropout
class NeuralTSAgent:
    def __init__(self, input_dim, output_dim, hidden_dim=64, lr=1e-3, dropout_passes=10, lambda_prior=1.0):
        self.output_dim = output_dim
        self.lambda_prior = lambda_prior
        self.dropout_passes = dropout_passes
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = MLP(input_dim, output_dim, hidden_dim).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.buffer = []
        self.batch_size = 32
        self.max_buffer_size = 10000

    def select_action(self, context):
        self.model.train()  # Enable dropout for stochasticity
        context_tensor = torch.tensor(context, dtype=torch.float32, device=self.device).unsqueeze(0)
        preds = []

        for _ in range(self.dropout_passes):
            out = self.model(context_tensor).detach().cpu().numpy()
            preds.append(out)

        preds = np.stack(preds)
        mean = preds.mean(axis=0)
        std = preds.std(axis=0)
        samples = mean + np.random.normal(0, 1 / np.sqrt(self.lambda_prior)) * std
        return int(np.argmax(samples))

    def store_transition(self, context, action, reward, next_state=None, done=None):
        if len(self.buffer) >= self.max_buffer_size:
            self.buffer.pop(0)
        self.buffer.append((context, action, reward))

    def train(self):
        if len(self.buffer) < self.batch_size:
            return

        batch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards = zip(*batch)
        states = torch.tensor(np.stack(states), dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.int64, device=self.device).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device).unsqueeze(1)

        q_vals = self.model(states).gather(1, actions)
        loss = nn.MSELoss()(q_vals, rewards)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
