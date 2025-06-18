# 📊 KeyRD Vectorized State Index Mapping

This file defines the position and meaning of each entry in the `vectorized_state` array returned by SimulatedUserEnv.

| Index | Feature                        | Description                                 |
|-------|--------------------------------|---------------------------------------------|
| 0     | age                            | User age                                    |
| 1     | sex_encoded                    | 0=female, 1=male, 2=nonbinary               |
| 2     | SES_encoded                    | 0=low, 1=medium, 2=high                     |
| 3     | gps_cluster                    | Clustered GPS location ID (0–4)             |
| 4     | location_type_encoded          | 0=home, 1=gym, ..., 5=outdoor               |
| 5     | time_of_day                    | 0–23                                        |
| 6     | day_of_week                    | 0=Monday through 6=Sunday                   |
| 7     | has_diabetes                   | 0/1 binary                                  |
| 8     | has_hypertension               | 0/1 binary                                  |
| 9     | num_meds                       | Integer count of meds                       |
| 10–12 | emr_vector[0..2]               | First 3 dimensions of EMR embedding         |
| 13    | steps_today                    | Pedometer value                             |
| 14    | hr                             | Heart rate                                  |
| 15    | hr_variability                 | HRV                                         |
| 16    | sleep_duration                 | Hours                                       |
| 17    | sleep_quality                  | 1–10 scale                                  |
| 18    | stress                         | 0–1                                         |
| 19    | fatigue                        | 0–1                                         |
| 20    | motivation                     | 0–1                                         |
| 21    | readiness                      | 0–1                                         |
| 22    | goal_salience                  | 0–1                                         |
| 23    | stage_of_change                | 1–5 (TTM model)                             |
| 24    | com_b.capability               | 0–1                                         |
| 25    | com_b.opportunity              | 0–1                                         |
| 26    | com_b.motivation               | 0–1                                         |
| 27    | nudge_acceptance_rate          | 0–1                                         |
| 28    | holiday_flag                   | 0/1 binary                                  |
| 29    | has_support_network            | 0/1 binary                                  |
| 30    | recent_life_event_encoded      | 0=None, 1=illness, 2=vacation, 3=stress     |
| 31    | cumulative_reward              | Float                                       |
| 32    | recent_reward                  | Float                                       |
| 33    | novelty_saturation             | 0–1                                         |
| 34    | engagement                     | 0–1                                         |
| 35    | last_action                    | Last action index (0–n_actions-1)           |
