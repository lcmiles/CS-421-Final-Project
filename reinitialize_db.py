from app import app
from models import db

# Ensure the app context is available
with app.app_context():
    # Drop all tables
    db.drop_all()
    print("Dropped all tables.")

    # Create all tables
    db.create_all()
    print("Created all tables.")