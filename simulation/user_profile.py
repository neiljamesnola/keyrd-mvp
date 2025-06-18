import random
import numpy as np

class UserProfile:
    def __init__(self, profile_type="default"):
        self.profile_type = profile_type
        self._initialize_traits()
        self.fatigue = 0.0
        self.engagement = 1.0  # normalized [0, 1]
        self.steps_since_start = 0

    def _initialize_traits(self):
        base_traits = {
            "resilience": 0.5,
            "dropout_baseline": 0.01,
            "nudge_sensitivity": 0.5,
            "attention_span": 0.5,
            "fatigue_accumulation": 0.02,
            "recovery_rate": 0.015,
        }

        profile_mods = {
            "fitness_junkie": {
                "resilience": 0.9,
                "nudge_sensitivity": 0.8,
                "attention_span": 0.7
            },
            "night_owl": {
                "resilience": 0.4,
                "nudge_sensitivity": 0.6,
                "attention_span": 0.4,
                "dropout_baseline": 0.015
            },
            "burnout_prone": {
                "resilience": 0.2,
                "fatigue_accumulation": 0.04,
                "attention_span": 0.3,
                "dropout_baseline": 0.02
            },
            "stress_eater": {
                "resilience": 0.3,
                "fatigue_accumulation": 0.035,
                "dropout_baseline": 0.018
            },
            "distractible": {
                "attention_span": 0.2,
                "nudge_sensitivity": 0.4,
                "resilience": 0.3
            },
        }

        self.traits = base_traits.copy()
        if self.profile_type in profile_mods:
            self.traits.update(profile_mods[self.profile_type])

        self.resilience_factor = self.traits["resilience"]

    def get_state(self):
        time_of_day = random.randint(0, 23)
        energy = max(0.0, 1.0 - self.fatigue + np.random.normal(0, 0.05))
        stress = min(1.0, max(0.0, 1.0 - self.resilience_factor + np.random.normal(0, 0.1)))
        return {
            "time": time_of_day,
            "energy": round(energy, 3),
            "stress": round(stress, 3)
        }

    def get_state_vector(self) -> np.ndarray:
        state = self.get_state()
        # Map features into numeric vector
        return np.array([
            state["time"] / 24.0,      # normalized time of day
            state["energy"],           # energy level
            state["stress"],           # stress level
            self.engagement,           # current engagement
            self.fatigue               # current fatigue
        ])

    def respond_to_nudge(self, arm: int) -> float:
        state = self.get_state()
        nudge_types = ["real_time", "email", "text"]
        nudge_type = nudge_types[arm % len(nudge_types)]
        relevant = self.is_nudge_contextually_relevant(nudge_type, state)

        # Simulate whether the user accepts the nudge
        acceptance_chance = self.traits["nudge_sensitivity"] * (0.7 if relevant else 0.3)
        accepted = random.random() < acceptance_chance

        self.receive_nudge(nudge_type, relevant, accepted)
        return float(self.get_engagement_score())

    def is_nudge_contextually_relevant(self, nudge_type, state):
        if nudge_type == "real_time":
            return state["energy"] > 0.5 and state["stress"] < 0.7
        elif nudge_type == "email":
            return state["time"] in range(9, 17)
        elif nudge_type == "text":
            return state["time"] in range(8, 22)
        elif nudge_type == "notification":
            return True
        return False

    def receive_nudge(self, nudge_type, relevant, accepted):
        if accepted:
            delta = self.traits["nudge_sensitivity"] * (1.0 if relevant else 0.5)
            self.engagement = min(1.0, self.engagement + delta * 0.05)
            self.fatigue = max(0.0, self.fatigue - self.traits["recovery_rate"])
        else:
            self.engagement = max(0.0, self.engagement - 0.05)
            self.fatigue += self.traits["fatigue_accumulation"]
        self.steps_since_start += 1

    def get_engagement_score(self):
        noise = np.random.normal(0, 0.02)
        return round(max(0.0, min(1.0, self.engagement + noise)), 3)

    def dropout_probability(self):
        fatigue_term = self.fatigue ** 2.2
        disengagement_term = (1.0 - self.engagement) ** 2.5
        base = self.traits["dropout_baseline"] * 1.5
        scaling = 1 + (self.steps_since_start / 80)
        raw_prob = base * scaling * fatigue_term * disengagement_term
        adjusted = raw_prob * (1 - self.resilience_factor * 0.7)
        return min(adjusted, 1.0)

    def is_active(self):
        return random.random() > self.dropout_probability()
