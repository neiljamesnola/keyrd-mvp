# scripts/test_db.py
import sys
import os
from sqlalchemy import text

# Add the root directory (keyrd_mvp) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("✅ DB object is initialized and working.")
    except Exception as e:
        print(f"❌ DB test failed: {e}")
