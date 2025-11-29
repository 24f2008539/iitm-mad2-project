from flask import Flask
from models.db import db
from models.admin import AdminModel

# Create a simple Flask app for context
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with the app
db.init_app(app)

# Create app context
with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Check if admin exists
    admin = AdminModel.find_by_username("admin")
    if admin:
        print("Admin 'admin' already exists")
    else:
        # Create new admin
        new_admin = AdminModel(username="admin", password="admin123", first_name="System", last_name="Admin")
        new_admin.save_to_db()
        print("Admin user 'admin' created successfully with password 'admin123'")
        
    # List all admins
    all_admins = AdminModel.query.all()
    print("\nAll admins in database:")
    for admin in all_admins:
        print(f"  - {admin.username} ({admin.first_name} {admin.last_name})")
