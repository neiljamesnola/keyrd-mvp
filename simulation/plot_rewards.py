import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to SQLite database
engine = create_engine('sqlite:///instance/keyrd.db')
df = pd.read_sql('SELECT * FROM nudge_log', con=engine)

# Preview the data
print(df.head())

# Plot cumulative reward
plt.figure(figsize=(10, 6))
plt.plot(pd.to_datetime(df['timestamp']), df['cumulative_reward'], marker='o')
plt.title('Cumulative Reward Over Time')
plt.xlabel('Time')
plt.ylabel('Cumulative Reward')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
