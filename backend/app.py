import os

# Fix Flask-Uploads compatibility with newer Werkzeug
import sys
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
sys.modules['werkzeug'].secure_filename = secure_filename
sys.modules['werkzeug'].FileStorage = FileStorage

from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_uploads import configure_uploads, patch_request_class
from flask_jwt_extended import JWTManager, get_raw_jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# import mysql.connector  
# import pymysql

from models.blacklist import BLACKLIST
from datetime import datetime

# Resources
from models.resources.doctor import (
    DoctorRegister,
    Doctor,
    DoctorLogin,
    DoctorList,
    DoctorPatient,
)
from models.resources.patient import (
    PatientRegister,
    Patient,
    PatientLogin,
    PatientList,
)
from models.resources.appointment import appointment, deleteAppointments
from models.resources.admin import AdminRegister, AdmingLogin
from models.resources.uploads import UploadImage, PatientImages, DeleteImage
from models.image_helper import IMAGE_SET
from models.resources.logout import Logout
from models.resources.analytics import Analytics
from models.resources.examination import (
    Examination,
    ExaminationList,
    ExaminationRegister,
    PatientExaminations,
)
from models.resources.contact_us import ContactUs, ContactUsList, ContactUsRegister
from models.resources.export import ExportTreatmentHistory, ExportStatus, PatientExports, DownloadExport


app = Flask(__name__, static_url_path="/static")
CORS(app)

# Use SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

app.config["UPLOADED_IMAGES_DEST"] = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = os.path.join("static", "exports")
app.secret_key = "my_secret_key"

patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)


@app.before_first_request
def create_tables():
    from models.db import db
    db.create_all()   # SQLite auto-creates tables


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user_claims = get_raw_jwt()["user_claims"]
    if user_claims["type"] == "doctor":
        return {"type": "doctor"}
    elif user_claims["type"] == "patient":
        return {"type": "patient"}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired.", "error": "Token expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"description": "Signature verification failed.", "error": "Invalid token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify({"description": "The token is not fresh.", "error": "fresh token required"}),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


# Resources
api.add_resource(DoctorRegister, "/doctor/register")
api.add_resource(Doctor, "/doctor/<int:doctor_id>")
api.add_resource(DoctorLogin, "/doctor/login")
api.add_resource(DoctorList, "/doctors")
api.add_resource(DoctorPatient, "/doctor/patients")

api.add_resource(PatientRegister, "/patient/register")
api.add_resource(Patient, "/patient/<int:patient_id>")
api.add_resource(PatientLogin, "/patient/login")
api.add_resource(PatientList, "/patients")

api.add_resource(appointment, "/appointments")
api.add_resource(deleteAppointments, "/appointments/<int:app_id>")

api.add_resource(AdminRegister, "/admin/register")
api.add_resource(AdmingLogin, "/admin/login")

api.add_resource(ExaminationRegister, "/appointments/<int:app_id>/examinations")
api.add_resource(PatientExaminations, "/patient/<int:patient_id>/examinations")
api.add_resource(ExaminationList, "/examinations")
api.add_resource(Examination, "/examination/<int:examination_id>")

api.add_resource(ContactUsRegister, "/contactus/form")
api.add_resource(ContactUs, "/contactus/<int:form_id>")
api.add_resource(ContactUsList, "/contactus/forms")

api.add_resource(UploadImage, "/upload/image/<int:patient_id>")
api.add_resource(PatientImages, "/images/<int:patient_id>")
api.add_resource(DeleteImage, "/image/delete/<int:patient_id>")

api.add_resource(Logout, "/logout")
api.add_resource(Analytics, "/analytics")

# Export resources
api.add_resource(ExportTreatmentHistory, "/patient/<int:patient_id>/export")
api.add_resource(ExportStatus, "/export/<int:export_id>")
api.add_resource(PatientExports, "/patient/<int:patient_id>/exports")
api.add_resource(DownloadExport, "/download/export/<int:export_id>")


if __name__ == "__main__":
    from models.db import db
    from models.email_helper import init_mail
    from models.jobs.scheduler import init_scheduler, add_daily_reminder_job, add_monthly_report_job, add_cleanup_job
    from models.jobs.tasks import send_daily_reminders, send_monthly_reports, cleanup_expired_exports
    
    db.init_app(app)
    
    # Initialize email service
    init_mail(app)
    
    # Initialize scheduler and add jobs
    scheduler = init_scheduler(app)
    add_daily_reminder_job(send_daily_reminders, hour=8, minute=0)  # 8 AM daily
    add_monthly_report_job(send_monthly_reports, day=1, hour=9, minute=0)  # 1st of month at 9 AM
    add_cleanup_job(cleanup_expired_exports, hour=2, minute=0)  # 2 AM daily
    
    print("\n" + "="*60)
    print("🏥 HOSPITAL INFORMATION SYSTEM - CARDIOLOGY DEPARTMENT")
    print("="*60)
    print("✓ Email service initialized")
    print("✓ Scheduler initialized with 3 jobs:")
    print("  - Daily reminders at 08:00")
    print("  - Monthly reports on 1st at 09:00")
    print("  - Cleanup expired exports at 02:00")
    print("="*60 + "\n")
    
    app.run(host="localhost", port=5000, debug=True)
