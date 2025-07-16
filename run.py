import sys
import os

# Add the root directory to sys.path so 'app' can be resolved
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
