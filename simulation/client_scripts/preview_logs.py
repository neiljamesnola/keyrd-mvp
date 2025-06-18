import csv
import os

def preview_csv(file_path, max_rows=10):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        print(f"\n📄 Previewing {file_path}:")
        for i, row in enumerate(reader):
            if i >= max_rows:
                print("... truncated ...")
                break
            print(row)

files = [
    "user_metadata_log.csv",
    "sensor_state_log.csv",
    "nudge_decision_log.csv",
    "nudge_feedback_log.csv"
]

for file in files:
    preview_csv(file)
