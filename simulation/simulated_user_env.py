import numpy as np
import random

class SimulatedUserEnv:
    def __init__(self, user_type="resilient", n_actions=4, max_steps=500):
        self.user_type = user_type
        self.n_actions = n_actions
        self.max_steps = max_steps
        self.state_dim = 36
        self.reset()

    def reset(self):
        self.t = 0
        self.done = False
        self.past_rewards = [0.0] * 5
        self.action_history = []
        self._initialize_user_profile()

        # Static demographics
        self.age = 54
        self.sex = "male"
        self.ses = "medium"

        # Contextual and environmental
        self.gps_cluster = np.random.randint(0, 5)
        self.location_type = "home"
        self.time_of_day = np.random.randint(0, 24)
        self.day_of_week = np.random.randint(0, 7)
        self.holiday_flag = 0
        self.has_support_network = 1
        self.recent_life_event = None

        # Medical
        self.has_diabetes = 0
        self.has_hypertension = 1
        self.num_meds = 3
        self.emr_vector = np.random.normal(0, 1, 5)

        # Meta state
        self.cumulative_reward = 0.0
        self.recent_reward = 0.0
        self.novelty_saturation = 0.0
        self.engagement = 1.0
        self.last_action = None

        return self._get_context()

    def _initialize_user_profile(self):
        profile_defaults = {
            "resilient": dict(fatigue=0.3, stress=0.3, motivation=0.8, readiness=0.8, goal_salience=0.7, nudge_acceptance_rate=0.85),
            "stress_eater": dict(fatigue=0.4, stress=0.8, motivation=0.6, readiness=0.6, goal_salience=0.5, nudge_acceptance_rate=0.7),
            "fatigue_sensitive": dict(fatigue=0.7, stress=0.4, motivation=0.6, readiness=0.6, goal_salience=0.5, nudge_acceptance_rate=0.7),
            "burnout_cyclic": dict(fatigue=0.7, stress=0.6, motivation=0.3, readiness=0.4, goal_salience=0.4, nudge_acceptance_rate=0.5),
            "novelty_seeker": dict(fatigue=0.3, stress=0.3, motivation=0.8, readiness=0.7, goal_salience=0.6, nudge_acceptance_rate=0.9),
            "rigid_responder": dict(fatigue=0.4, stress=0.4, motivation=0.5, readiness=0.6, goal_salience=0.5, nudge_acceptance_rate=0.2),
            "avoidant_withdrawer": dict(fatigue=0.5, stress=0.7, motivation=0.3, readiness=0.2, goal_salience=0.4, nudge_acceptance_rate=0.2),
            "chaotic_highvariance": dict(
                fatigue=np.random.uniform(0.1, 0.9),
                stress=np.random.uniform(0.1, 0.9),
                motivation=np.random.uniform(0.2, 0.8),
                readiness=np.random.uniform(0.2, 0.8),
                goal_salience=np.random.uniform(0.2, 0.8),
                nudge_acceptance_rate=np.random.uniform(0.2, 0.9),
            )
        }

        defaults = profile_defaults.get(self.user_type, profile_defaults["resilient"])
        for k, v in defaults.items():
            setattr(self, k, v)

        self.stage_of_change = random.randint(1, 5)
        self.com_b = {
            "capability": np.random.uniform(0.4, 0.9),
            "opportunity": np.random.uniform(0.4, 0.9),
            "motivation": self.motivation
        }
        self.cycle_counter = 0  # For cyclical profiles

    def _get_context(self):
        noise = np.random.uniform(0, 1, 2)
        return np.array(self._vectorize_state()[:self.state_dim] + list(noise))

    def _vectorize_state(self):
        return [
            self.age,
            {"female": 0, "male": 1, "nonbinary": 2}.get(self.sex, 1),
            {"low": 0, "medium": 1, "high": 2}.get(self.ses, 1),
            self.gps_cluster,
            {"home": 0, "gym": 1, "store": 2, "work": 3, "transit": 4, "outdoor": 5}.get(self.location_type, 0),
            self.time_of_day,
            self.day_of_week,
            self.has_diabetes,
            self.has_hypertension,
            self.num_meds,
            *self.emr_vector[:3],
            self.steps,
            self.hr,
            self.hr_variability,
            self.sleep_duration,
            self.sleep_quality,
            self.stress,
            self.fatigue,
            self.motivation,
            self.readiness,
            self.goal_salience,
            self.stage_of_change,
            self.com_b["capability"],
            self.com_b["opportunity"],
            self.com_b["motivation"],
            self.nudge_acceptance_rate,
            self.holiday_flag,
            self.has_support_network,
            {None: 0, "illness": 1, "vacation": 2, "family_stress": 3}.get(self.recent_life_event, 0),
            self.cumulative_reward,
            self.recent_reward,
            self.novelty_saturation,
            self.engagement,
            self.last_action if self.last_action is not None else -1
        ]

    def _calculate_reward(self, action):
        trend = np.mean(self.past_rewards[-3:])
        fatigue_penalty = 0.2 * self.fatigue
        stress_penalty = 0.2 * self.stress
        novelty_penalty = 0.1 * self.novelty_saturation
        bonus = 0.1 if ((action == 3 and self.stress > 0.6) or (action == 2 and self.goal_salience < 0.4)) else 0.0

        base = (
            0.4 * self.motivation +
            0.3 * self.readiness +
            0.1 * trend +
            bonus -
            fatigue_penalty -
            stress_penalty -
            novelty_penalty
        )

        if self.user_type == "stress_eater" and self.stress > 0.7:
            base *= 0.6
        if self.user_type == "fatigue_sensitive" and self.fatigue > 0.7:
            base *= 0.6

        return float(np.clip(base + np.random.normal(0, 0.03), 0, 1))

    def _update_state(self, action):
        self.steps = np.clip(self.steps + np.random.normal(300, 800), 0, 20000)
        self.fatigue += 0.01 + 0.01 * (1 - self.sleep_quality / 10)
        self.stress = np.clip(self.stress + np.random.normal(0, 0.03), 0, 1)
        self.sleep_quality += np.random.normal(0, 0.3)
        self.sleep_duration += np.random.normal(0, 0.2)
        self.hr += np.random.normal(0, 1)
        self.hr_variability += np.random.normal(0, 1)
        self.gps_cluster = np.random.randint(0, 5)

        if action == self.last_action:
            self.novelty_saturation += 0.03
        else:
            self.novelty_saturation *= 0.9

        if action == 0:
            self.fatigue -= 0.05
        elif action == 1:
            self.motivation += 0.05 * self.com_b["capability"]
        elif action == 2:
            self.goal_salience += 0.04
        elif action == 3:
            self.stress -= 0.03
            self.readiness += 0.03

        # Archetype-specific effects
        if self.user_type == "burnout_cyclic":
            self.cycle_counter += 1
            if self.cycle_counter % 30 == 0:
                self.motivation = max(0.2, self.motivation - 0.3)
                self.fatigue = min(1.0, self.fatigue + 0.2)
                self.stress = min(1.0, self.stress + 0.2)
        elif self.user_type == "novelty_seeker":
            if action == self.last_action:
                self.engagement -= 0.03
            else:
                self.engagement += 0.02
        elif self.user_type == "rigid_responder":
            if action != self.last_action:
                self.engagement -= 0.02
        elif self.user_type == "avoidant_withdrawer":
            if self.t % 10 == 0:
                self.readiness = max(0.1, self.readiness - 0.05)
                self.nudge_acceptance_rate *= 0.98
        elif self.user_type == "chaotic_highvariance":
            for attr in ["motivation", "readiness", "stress", "goal_salience"]:
                val = getattr(self, attr)
                noise = np.random.normal(0, 0.1)
                setattr(self, attr, np.clip(val + noise, 0, 1))

        if self.recent_reward > 0.7:
            self.stage_of_change = min(5, self.stage_of_change + 1)
        elif self.recent_reward < 0.3:
            self.stage_of_change = max(1, self.stage_of_change - 1)

        # Clamp physiological variables
        self.fatigue = np.clip(self.fatigue, 0, 1)
        self.motivation = np.clip(self.motivation, 0, 1)
        self.goal_salience = np.clip(self.goal_salience, 0, 1)
        self.readiness = np.clip(self.readiness, 0, 1)
        self.sleep_quality = np.clip(self.sleep_quality, 1, 10)
        self.sleep_duration = np.clip(self.sleep_duration, 2, 10)
        self.hr = np.clip(self.hr, 50, 120)
        self.hr_variability = np.clip(self.hr_variability, 10, 100)

    def _dropout_probability(self):
        a, b, c, d = 3.2, 0.002, 0.08, 0.25
        logit = (
            -a * self.cumulative_reward +
            b * self.t +
            c * self.stress +
            1.5 * self.novelty_saturation -
            2.0 * self.engagement +
            d * np.std(self.past_rewards)
        )
        return 1 / (1 + np.exp(-logit)) if -50 < logit < 50 else float(logit > 50)

    def step(self, action):
        self._update_state(action)
        reward = self._calculate_reward(action)
        self.past_rewards.append(reward)
        self.recent_reward = reward
        self.cumulative_reward += reward
        self.engagement = np.clip(self.engagement + 0.02 * reward - 0.02 * self.fatigue, 0, 1)

        self.action_history.append(action)
        self.last_action = action
        self.t += 1
        dropout = np.random.rand() < self._dropout_probability()
        self.done = dropout or self.engagement < 0.05 or self.t >= self.max_steps

        return self._get_context(), reward, self.done

    def to_json_state(self):
        return {
            "archetype": self.user_type,
            "demographics": {
                "age": self.age,
                "sex": self.sex,
                "socioeconomic_status": self.ses
            },
            "location_context": {
                "gps_cluster": self.gps_cluster,
                "location_type": self.location_type,
                "time_of_day": self.time_of_day,
                "day_of_week": self.day_of_week
            },
            "medical_context": {
                "has_diabetes": self.has_diabetes,
                "has_hypertension": self.has_hypertension,
                "num_meds": self.num_meds,
                "emr_vector": self.emr_vector.tolist()
            },
            "biosensor_signals": {
                "steps_today": self.steps,
                "hr": self.hr,
                "hr_variability": self.hr_variability,
                "sleep_duration": self.sleep_duration,
                "sleep_quality": self.sleep_quality,
                "stress": self.stress,
                "fatigue": self.fatigue
            },
            "behavioral_state": {
                "motivation": self.motivation,
                "readiness": self.readiness,
                "goal_salience": self.goal_salience,
                "stage_of_change": self.stage_of_change,
                "com_b": self.com_b,
                "nudge_acceptance_rate": self.nudge_acceptance_rate
            },
            "life_context": {
                "holiday_flag": self.holiday_flag,
                "has_support_network": self.has_support_network,
                "recent_life_event": self.recent_life_event
            },
            "meta_state": {
                "cumulative_reward": self.cumulative_reward,
                "recent_reward": self.recent_reward,
                "novelty_saturation": self.novelty_saturation,
                "engagement": self.engagement,
                "last_action": self.last_action
            },
            "vectorized_state": self._vectorize_state()
        }
