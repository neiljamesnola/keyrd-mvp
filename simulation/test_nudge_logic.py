import unittest
import os  # ✅ ADD THIS
from simulation import nudge_logic as nl

class TestNudgeLogic(unittest.TestCase):

    def setUp(self):
        self.state_morning = {"time_of_day": "morning"}
        self.state_night = {"time_of_day": "night"}

    def test_choose_nudge_random(self):
        nudge = nl.choose_nudge(self.state_morning, strategy="random")
        self.assertIn(nudge, nl.NUDGE_TYPES)

    def test_choose_nudge_epsilon_greedy(self):
        nudge = nl.choose_nudge(self.state_morning, strategy="epsilon_greedy", epsilon=0.5)
        self.assertIn(nudge, nl.NUDGE_TYPES)

    def test_is_contextually_relevant(self):
        self.assertTrue(nl.is_contextually_relevant("reminder", self.state_morning))
        self.assertFalse(nl.is_contextually_relevant("reminder", self.state_night))

    def test_simulate_response_output(self):
        nudge = "alert"
        response = nl.simulate_response(nudge, self.state_morning)
        self.assertIn(response, ["accepted", "ignored", "annoyed"])

    def test_get_reward_logic(self):
        reward = nl.get_reward("accepted", "reminder", self.state_morning)
        self.assertEqual(reward, 1.0)

        reward = nl.get_reward("accepted", "alert", self.state_morning)
        self.assertEqual(reward, 0.6)

        reward = nl.get_reward("ignored", "alert", self.state_morning)
        self.assertEqual(reward, -0.1)

        reward = nl.get_reward("annoyed", "alert", self.state_morning)
        self.assertEqual(reward, -0.5)

    def test_update_q_value(self):
        state = self.state_morning
        action = "tip"
        reward = 0.5
        nl.update_q_value(state, action, reward)
        updated_q = nl.Q_TABLE[nl.normalize_state(state)][action]
        self.assertIsInstance(updated_q, float)

    def test_q_table_export_import(self):
        nl.export_q_table_to_csv("output/test_q_table.csv")
        self.assertTrue(os.path.exists("output/test_q_table.csv"))

        # simulate loading
        nl.load_q_data("output/q_data.json")  # should not raise

if __name__ == '__main__':
    unittest.main()
