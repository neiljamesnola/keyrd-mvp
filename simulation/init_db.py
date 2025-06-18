# init_db.py

from app import app, db
from models import NudgeLog, FeedbackLog  # optional: ensures tables are registered

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()  # optional reset
        db.create_all()
        print("Database initialized at: instance/keyrd.db")
