from models import db, create_app, NudgeLog
from datetime import datetime, timedelta
import random

app = create_app()

def seed_logs():
    with app.app_context():
        print("Seeding NudgeLog with synthetic data...")
        db.session.query(NudgeLog).delete()

        base_time = datetime.utcnow()
        cumulative_reward = 0.0

        for i in range(50):
            timestamp = base_time + timedelta(minutes=i)
            user_id = "sim_user_1"
            state = random.choice(["neutral", "active", "tired"])
            nudge_type = random.choice(["walk", "relax", "sleep"])
            nudge_text = f"Synthetic nudge message {i+1}"
            response = random.choice(["accept", "reject", "ignore"])
            reward = round(random.uniform(-0.5, 1.0), 2)
            cumulative_reward += reward

            log = NudgeLog(
                timestamp=timestamp,
                user_id=user_id,
                state=state,
                nudge_type=nudge_type,
                nudge_text=nudge_text,
                response=response,
                reward=reward,
                cumulative_reward=round(cumulative_reward, 2)
            )
            db.session.add(log)

        db.session.commit()
        print("Seeding complete. 50 entries added.")

if __name__ == "__main__":
    seed_logs()
