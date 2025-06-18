# analyze_logs.py

import pandas as pd
import matplotlib.pyplot as plt
from models import db, create_app, NudgeLog

app = create_app()

def load_logs():
    with app.app_context():
        logs = NudgeLog.query.order_by(NudgeLog.timestamp).all()
        if not logs:
            print("No logs found.")
            return pd.DataFrame()
        return pd.DataFrame([{
            'timestamp': log.timestamp,
            'user_id': log.user_id,
            'state': log.state,
            'nudge_type': log.nudge_type,
            'nudge_text': log.nudge_text,
            'response': log.response,
            'reward': log.reward,
            'cumulative_reward': log.cumulative_reward
        } for log in logs])

def plot_rewards(df):
    if df.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['cumulative_reward'], marker='o')
    plt.title('Cumulative Reward Over Time')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Reward')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load_logs()
    print(df.head())
    plot_rewards(df)
