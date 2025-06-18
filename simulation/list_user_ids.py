import csv

with open("user_metadata_log.csv", newline="") as file:
    reader = csv.DictReader(file)
    user_ids = [row["user_id"] for row in reader]

print("Registered User IDs:")
for uid in user_ids:
    print(uid)
