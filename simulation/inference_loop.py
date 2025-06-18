from user_profile import UserProfile
from bandit_linucb import LinUCB
import numpy as np
import time

# Initialize
user = UserProfile(profile_type='stress_eater')
linucb = LinUCB(num_arms=3, context_dim=5, alpha=0.1)
n_steps = 50

for t in range(n_steps):
    context = user.get_state_vector()
    chosen_arm = linucb.select_arm(context)
    reward = user.respond_to_nudge(chosen_arm)
    linucb.update(chosen_arm, context, reward)

    print(f"[Step {t}] Arm: {chosen_arm}, Reward: {reward:.2f}, Engagement: {user.engagement:.2f}")
    time.sleep(0.1)
