from models.db import db
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class AppointmentModel(db.Model):
    __tablename__ = "Appointments"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    created_at = db.Column(db.Date)
    description = db.Column(db.String(5000))

    doctor_id = db.Column(db.Integer, db.ForeignKey("Doctors.id", ondelete="SET NULL"))
    patient_id = db.Column(
        db.Integer, db.ForeignKey("Patients.id", ondelete="SET NULL")
    )
    patient_username = db.Column(db.String(80))
    doctor_username = db.Column(db.String(80))

    doctor = db.relationship("DoctorModel")
    patient = db.relationship("PatientModel")

    def __init__(self, date, doctor_id, patient_id, created_at, description,patient_username,doctor_username):
        self.date = date
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.patient_username = patient_username
        self.doctor_username = doctor_username
        self.created_at = created_at
        self.description = description

    def json(self):
        return {
            "_id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "patient_id": self.patient_id,
            "patient_username": self.patient_username,
            "doctor_id": self.doctor_id,
            "doctor_username": self.doctor_username,
            "date_of_reservation": self.created_at.strftime("%Y-%m-%d"),
            "description": self.description,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    @classmethod
    def main(cls, start_time):
        """
        Google Calendar integration - currently disabled to avoid authentication issues.
        Enable this when you have properly configured Google OAuth credentials.
        """
        pass