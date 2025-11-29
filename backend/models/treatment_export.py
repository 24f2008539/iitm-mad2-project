"""
TreatmentExport Model - Tracks patient export history and status
"""
from models.db import db
from datetime import datetime, timedelta
from enum import Enum


class ExportStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TreatmentExportModel(db.Model):
    __tablename__ = "TreatmentExports"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("Patients.id", ondelete="CASCADE"))
    export_type = db.Column(db.String(50), default="csv")  # csv, pdf, etc
    status = db.Column(db.String(20), default="pending")  # pending, processing, completed, failed
    file_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime)  # Link expires after 7 days
    error_message = db.Column(db.String(500), nullable=True)

    patient = db.relationship("PatientModel")

    def __init__(self, patient_id, export_type="csv"):
        self.patient_id = patient_id
        self.export_type = export_type
        self.status = "pending"
        self.created_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(days=7)

    def json(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "export_type": self.export_type,
            "status": self.status,
            "file_path": self.file_path,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "completed_at": self.completed_at.strftime("%Y-%m-%d %H:%M:%S") if self.completed_at else None,
            "expires_at": self.expires_at.strftime("%Y-%m-%d %H:%M:%S") if self.expires_at else None,
            "is_expired": datetime.utcnow() > self.expires_at,
            "error_message": self.error_message,
        }

    def mark_processing(self):
        """Mark export as currently processing"""
        self.status = "processing"
        db.session.commit()

    def mark_completed(self, file_path):
        """Mark export as completed and store file path"""
        self.status = "completed"
        self.file_path = file_path
        self.completed_at = datetime.utcnow()
        db.session.commit()

    def mark_failed(self, error_message):
        """Mark export as failed with error message"""
        self.status = "failed"
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, export_id):
        return cls.query.filter_by(id=export_id).first()

    @classmethod
    def find_by_patient_id(cls, patient_id):
        """Get all exports for a patient"""
        return cls.query.filter_by(patient_id=patient_id).order_by(cls.created_at.desc()).all()

    @classmethod
    def find_pending(cls):
        """Get all pending exports"""
        return cls.query.filter_by(status="pending").all()

    @classmethod
    def cleanup_expired(cls):
        """Delete expired exports older than 7 days"""
        expired_exports = cls.query.filter(cls.expires_at < datetime.utcnow()).all()
        for export in expired_exports:
            export.delete_from_db()
        return len(expired_exports)
