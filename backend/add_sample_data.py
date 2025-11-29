from flask import Flask
from models.db import db
from models.admin import AdminModel
from models.doctor import DoctorModel
from models.patient import PatientModel
from datetime import datetime, date

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
    
    print("=" * 60)
    print("ADDING SAMPLE DATA TO DATABASE")
    print("=" * 60)
    
    # ADD ADMINS
    print("\n--- ADMINS ---")
    admins_data = [
        {"username": "admin", "password": "admin123", "first_name": "System", "last_name": "Admin"},
        {"username": "admin2", "password": "admin456", "first_name": "John", "last_name": "Manager"},
        {"username": "admin3", "password": "admin789", "first_name": "Sarah", "last_name": "Supervisor"},
    ]
    
    for admin_data in admins_data:
        if not AdminModel.find_by_username(admin_data["username"]):
            admin = AdminModel(**admin_data)
            admin.save_to_db()
            print(f"✓ Created admin: {admin_data['username']} / {admin_data['password']}")
        else:
            print(f"✗ Admin {admin_data['username']} already exists")
    
    # ADD DOCTORS
    print("\n--- DOCTORS ---")
    doctors_data = [
        {
            "username": "dr_ahmed",
            "password": "doc123",
            "first_name": "Ahmed",
            "last_name": "Ali",
            "email": "ahmed@hospital.com",
            "mobile": "0123456789",
            "gender": 0,  # male
            "birthdate": date(1975, 5, 15),
            "address": "Cairo, Egypt",
            "created_at": date.today(),
            "specialization": "Cardiology"
        },
        {
            "username": "dr_fatima",
            "password": "doc456",
            "first_name": "Fatima",
            "last_name": "Hassan",
            "email": "fatima@hospital.com",
            "mobile": "0987654321",
            "gender": 1,  # female
            "birthdate": date(1982, 3, 20),
            "address": "Cairo, Egypt",
            "created_at": date.today(),
            "specialization": "Interventional Cardiology"
        },
        {
            "username": "dr_karim",
            "password": "doc789",
            "first_name": "Karim",
            "last_name": "Mohamed",
            "email": "karim@hospital.com",
            "mobile": "0555555555",
            "gender": 0,  # male
            "birthdate": date(1978, 7, 10),
            "address": "Alexandria, Egypt",
            "created_at": date.today(),
            "specialization": "Cardiology"
        },
        {
            "username": "dr_sara",
            "password": "doc999",
            "first_name": "Sara",
            "last_name": "Ibrahim",
            "email": "sara@hospital.com",
            "mobile": "0666666666",
            "gender": 1,  # female
            "birthdate": date(1985, 12, 5),
            "address": "Giza, Egypt",
            "created_at": date.today(),
            "specialization": "Pediatric Cardiology"
        },
    ]
    
    for doctor_data in doctors_data:
        if not DoctorModel.find_by_username(doctor_data["username"]):
            doctor = DoctorModel(**doctor_data)
            doctor.save_to_db()
            print(f"✓ Created doctor: {doctor_data['first_name']} {doctor_data['last_name']} ({doctor_data['username']}) - {doctor_data['specialization']}")
        else:
            print(f"✗ Doctor {doctor_data['username']} already exists")
    
    # ADD PATIENTS
    print("\n--- PATIENTS ---")
    patients_data = [
        {
            "username": "patient_001",
            "password": "pat123",
            "first_name": "Ali",
            "last_name": "Ahmed",
            "email": "ali.ahmed@email.com",
            "mobile": "0123456789",
            "gender": 0,  # male
            "birthdate": date(1979, 6, 12),
            "address": "Cairo, Egypt",
            "created_at": date.today()
        },
        {
            "username": "patient_002",
            "password": "pat456",
            "first_name": "Mona",
            "last_name": "Hassan",
            "email": "mona.hassan@email.com",
            "mobile": "0987654321",
            "gender": 1,  # female
            "birthdate": date(1986, 8, 22),
            "address": "Alexandria, Egypt",
            "created_at": date.today()
        },
        {
            "username": "patient_003",
            "password": "pat789",
            "first_name": "Mohamed",
            "last_name": "Ibrahim",
            "email": "mohamed.ibrahim@email.com",
            "mobile": "0555555555",
            "gender": 0,  # male
            "birthdate": date(1964, 11, 3),
            "address": "Giza, Egypt",
            "created_at": date.today()
        },
        {
            "username": "patient_004",
            "password": "pat999",
            "first_name": "Noor",
            "last_name": "Ali",
            "email": "noor.ali@email.com",
            "mobile": "0666666666",
            "gender": 1,  # female
            "birthdate": date(1992, 1, 14),
            "address": "Cairo, Egypt",
            "created_at": date.today()
        },
        {
            "username": "patient_005",
            "password": "pat111",
            "first_name": "Hassan",
            "last_name": "Khaled",
            "email": "hassan.khaled@email.com",
            "mobile": "0777777777",
            "gender": 0,  # male
            "birthdate": date(1964, 4, 8),
            "address": "Mansoura, Egypt",
            "created_at": date.today()
        },
        {
            "username": "patient_006",
            "password": "pat222",
            "first_name": "Layla",
            "last_name": "Omar",
            "email": "layla.omar@email.com",
            "mobile": "0888888888",
            "gender": 1,  # female
            "birthdate": date(1982, 9, 28),
            "address": "Cairo, Egypt",
            "created_at": date.today()
        },
    ]
    
    for patient_data in patients_data:
        if not PatientModel.find_by_username(patient_data["username"]):
            patient = PatientModel(**patient_data)
            patient.save_to_db()
            print(f"✓ Created patient: {patient_data['first_name']} {patient_data['last_name']} ({patient_data['username']})")
        else:
            print(f"✗ Patient {patient_data['username']} already exists")
    
    # DISPLAY SUMMARY
    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)
    
    admins = AdminModel.query.all()
    doctors = DoctorModel.query.all()
    patients = PatientModel.query.all()
    
    print(f"\nTotal Admins: {len(admins)}")
    for admin in admins:
        print(f"  - {admin.username} ({admin.first_name} {admin.last_name})")
    
    print(f"\nTotal Doctors: {len(doctors)}")
    for doctor in doctors:
        print(f"  - {doctor.username} ({doctor.first_name} {doctor.last_name})")
    
    print(f"\nTotal Patients: {len(patients)}")
    for patient in patients:
        print(f"  - {patient.username} ({patient.first_name} {patient.last_name})")
    
    print("\n" + "=" * 60)
    print("✓ Sample data added successfully!")
    print("=" * 60)
    print("\nYou can now login with any of these credentials:\n")
    print("ADMIN CREDENTIALS:")
    print("  Username: admin, Password: admin123")
    print("  Username: admin2, Password: admin456")
    print("  Username: admin3, Password: admin789")
    print("\nDOCTOR CREDENTIALS:")
    print("  Username: dr_ahmed, Password: doc123")
    print("  Username: dr_fatima, Password: doc456")
    print("  Username: dr_karim, Password: doc789")
    print("  Username: dr_sara, Password: doc999")
    print("\nPATIENT CREDENTIALS:")
    print("  Username: patient_001, Password: pat123")
    print("  Username: patient_002, Password: pat456")
    print("  Username: patient_003, Password: pat789")
    print("  Username: patient_004, Password: pat999")
    print("  Username: patient_005, Password: pat111")
    print("  Username: patient_006, Password: pat222")
