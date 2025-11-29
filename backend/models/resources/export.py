"""
Export Resource - Handle CSV export requests from frontend
"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.treatment_export import TreatmentExportModel
from models.patient import PatientModel
from models.jobs.tasks import process_pending_exports
import os
from flask import send_file, current_app
from datetime import datetime


class ExportTreatmentHistory(Resource):
    """
    Trigger an export of patient's treatment history
    POST /patient/<patient_id>/export
    """
    
    @jwt_required
    def post(self, patient_id):
        # Verify patient is requesting their own export
        current_patient_id = get_jwt_identity()
        
        if current_patient_id != patient_id:
            return {"message": "Unauthorized"}, 403
        
        # Verify patient exists
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404
        
        try:
            # Create new export record
            export = TreatmentExportModel(patient_id=patient_id, export_type="csv")
            export.save_to_db()
            
            print(f"✓ Export job created for patient {patient_id}")
            
            # Process the export immediately (can be queued to a background worker in production)
            process_pending_exports()
            
            return {
                "message": "Export request received",
                "export_id": export.id,
                "status": export.status,
                "created_at": export.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }, 202
            
        except Exception as e:
            return {"message": f"Error creating export: {str(e)}"}, 500


class ExportStatus(Resource):
    """
    Get status of an export
    GET /export/<export_id>
    """
    
    @jwt_required
    def get(self, export_id):
        export = TreatmentExportModel.find_by_id(export_id)
        
        if not export:
            return {"message": "Export not found"}, 404
        
        # Verify patient is requesting their own export status
        current_patient_id = get_jwt_identity()
        if current_patient_id != export.patient_id:
            return {"message": "Unauthorized"}, 403
        
        return export.json(), 200


class PatientExports(Resource):
    """
    Get all exports for a patient
    GET /patient/<patient_id>/exports
    """
    
    @jwt_required
    def get(self, patient_id):
        # Verify patient is requesting their own exports
        current_patient_id = get_jwt_identity()
        
        if current_patient_id != patient_id:
            return {"message": "Unauthorized"}, 403
        
        exports = TreatmentExportModel.find_by_patient_id(patient_id)
        
        return {
            "exports": [export.json() for export in exports],
            "total": len(exports)
        }, 200


class DownloadExport(Resource):
    """
    Download export file
    GET /download/export/<export_id>
    """
    
    def get(self, export_id):
        export = TreatmentExportModel.find_by_id(export_id)
        
        if not export:
            return {"message": "Export not found"}, 404
        
        # Check if expired
        if export.is_expired:
            return {"message": "Export link has expired"}, 410
        
        # Check if completed
        if export.status != "completed":
            return {"message": f"Export is {export.status}, cannot download"}, 400
        
        # Check if file exists
        if not os.path.exists(export.file_path):
            return {"message": "Export file not found"}, 404
        
        try:
            return send_file(
                export.file_path,
                as_attachment=True,
                download_name=os.path.basename(export.file_path)
            )
        except Exception as e:
            return {"message": f"Error downloading file: {str(e)}"}, 500
