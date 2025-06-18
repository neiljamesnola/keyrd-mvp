# external_apis.py

import random
import datetime

def fetch_nhanes_mock():
    """Simulates fetching health indicators from NHANES."""
    return {
        'bmi': round(random.uniform(18.5, 35.0), 1),
        'cholesterol': random.randint(150, 250),
        'blood_pressure': f"{random.randint(100, 140)}/{random.randint(70, 90)}",
        'glucose': random.randint(70, 120),
        'timestamp': datetime.datetime.now().isoformat()
    }

def fetch_garmin_mock():
    """Simulates fetching real-time data from Garmin."""
    return {
        'heart_rate': random.randint(60, 120),
        'sleep_hours': round(random.uniform(4.0, 9.0), 1),
        'steps': random.randint(1000, 12000),
        'active_minutes': random.randint(10, 120),
        'timestamp': datetime.datetime.now().isoformat()
    }

def merge_external_data(nhanes, garmin):
    """Combines mock NHANES and Garmin data for logging or ML input."""
    return {
        'bmi': nhanes['bmi'],
        'cholesterol': nhanes['cholesterol'],
        'blood_pressure': nhanes['blood_pressure'],
        'glucose': nhanes['glucose'],
        'heart_rate': garmin['heart_rate'],
        'sleep_hours': garmin['sleep_hours'],
        'steps': garmin['steps'],
        'active_minutes': garmin['active_minutes'],
        'timestamp': datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    nhanes = fetch_nhanes_mock()
    garmin = fetch_garmin_mock()
    combined = merge_external_data(nhanes, garmin)
    print("Mock NHANES Data:", nhanes)
    print("Mock Garmin Data:", garmin)
    print("Merged Data:", combined)
