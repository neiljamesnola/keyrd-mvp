import random
import datetime

class SimulatedUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = 'neutral'
        self.energy_level = 0.5  # [0, 1]
        self.sleep_quality = 0.5
        self.stress_level = 0.5
        self.activity_level = 0.5
        self.nutrition_score = 0.5
        self.history = []

    def simulate_day(self):
        self.sleep_quality = max(0, min(1, random.gauss(self.sleep_quality, 0.05)))
        self.stress_level = max(0, min(1, random.gauss(self.stress_level, 0.1)))
        self.activity_level = max(0, min(1, random.gauss(self.activity_level, 0.1)))
        self.nutrition_score = max(0, min(1, random.gauss(self.nutrition_score, 0.1)))

        self.energy_level = (
            0.4 * self.sleep_quality -
            0.3 * self.stress_level +
            0.2 * self.activity_level +
            0.1 * self.nutrition_score
        )
        self.energy_level = max(0, min(1, self.energy_level))

        if self.energy_level > 0.7:
            self.state = 'energized'
        elif self.energy_level < 0.3:
            self.state = 'tired'
        else:
            self.state = 'neutral'

        self.history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'energy': self.energy_level,
            'sleep': self.sleep_quality,
            'stress': self.stress_level,
            'activity': self.activity_level,
            'nutrition': self.nutrition_score,
            'state': self.state
        })

    def receive_nudge(self, nudge_type):
        if nudge_type == 'sleep':
            self.sleep_quality = min(1.0, self.sleep_quality + 0.1)
        elif nudge_type == 'relax':
            self.stress_level = max(0.0, self.stress_level - 0.1)
        elif nudge_type == 'walk':
            self.activity_level = min(1.0, self.activity_level + 0.1)
        elif nudge_type == 'nutrition':
            self.nutrition_score = min(1.0, self.nutrition_score + 0.1)
