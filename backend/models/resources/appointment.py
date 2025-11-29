from flask_restful import Resource, reqparse
from models.appointment import AppointmentModel
from models.examination import ExaminationModel
from datetime import datetime
from models.doctor import DoctorModel
from models.patient import PatientModel
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt_claims,
)


class appointment(Resource):
    appointment_parser = reqparse.RequestParser()
    appointment_parser.add_argument(
        "doctor_id", type=str, required=True, help="This field cannot be blank."
    )
    appointment_parser.add_argument("description", type=str, required=False)
    appointment_parser.add_argument("patient_id", type=int, required=False)
    appointment_parser.add_argument(
        "date", type=str, required=True, help="This field cannot be blank."
    )

    @classmethod
    @jwt_required
    def post(cls):
        claims = get_jwt_claims()
        if claims["type"] != "patient":
            return {"message": "Access denied"}, 401

        data = cls.appointment_parser.parse_args()
        identity = get_jwt_identity()

        # Validate date
        if not data["date"] or data["date"].isspace():
            return {"message": "Date field cannot be empty"}, 400

        # Convert and validate date format
        try:
            y1, m1, d1 = [int(x) for x in data["date"].split("-")]
            app_date = datetime(y1, m1, d1).date()
        except (ValueError, IndexError):
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        # Check if date is in the future
        created_at = datetime.now().date()
        if app_date < created_at:
            return {"message": "Cannot book appointment in the past"}, 400

        # Convert doctor_id to integer
        try:
            doctor_id = int(data["doctor_id"])
        except (ValueError, TypeError):
            return {"message": "Invalid doctor ID"}, 400

        # Check if doctor exists
        doctor = DoctorModel.find_by_id(doctor_id)
        if not doctor:
            return {"message": "Doctor not found"}, 404

        # Get patient info
        patient = PatientModel.find_by_id(identity)
        if not patient:
            return {"message": "Patient not found"}, 404

        # Check if patient already has appointment on same date
        apps_date = AppointmentModel.find_by_date(app_date)
        for app in apps_date:
            if app.patient_id == identity:
                return {"message": "You already have an appointment on this date"}, 400

        # Prepare appointment data
        appointment_data = {
            'date': app_date,
            'doctor_id': doctor_id,
            'patient_id': identity,
            'created_at': created_at,
            'description': data.get('description', ''),
            'patient_username': patient.username,
            'doctor_username': doctor.username
        }

        try:
            # Trigger Google Calendar integration (currently disabled)
            AppointmentModel.main(app_date)
            
            # Create appointment
            appointment = AppointmentModel(**appointment_data)
            appointment.save_to_db()
            return {"message": "Appointment created successfully."}, 201
        except Exception as e:
            print(f"Error creating appointment: {str(e)}")
            return {"message": f"Error creating appointment: {str(e)}"}, 500

        return {"message": "Appointment created successfully."}, 201

    @classmethod
    @jwt_required
    def get(cls):
        identity = get_jwt_identity()
        claims = get_jwt_claims()

        if claims["type"] == "doctor":
            doctor_appointments = DoctorModel.find_by_id(identity).appointments
            
            # Filter out appointments that have examinations
            pending_appointments = []
            for appointment in doctor_appointments:
                # Check if this appointment has an examination
                examination = ExaminationModel.query.filter_by(appointment_id=appointment.id).first()
                if not examination:  # Only include if no examination exists
                    pending_appointments.append(appointment)
            
            doctorapp = [appointment.json() for appointment in pending_appointments]
            return doctorapp, 200

        elif claims["type"] == "patient":
            patient_appointments = PatientModel.find_by_id(identity).appointments

            patientapp = [appointment.json() for appointment in patient_appointments]
            return patientapp

        else:
            appointments = AppointmentModel.find_all()
            appointments_list = [appointment.json() for appointment in appointments]
            return appointments_list, 200


class deleteAppointments(Resource):
    @classmethod
    @jwt_required
    def delete(cls, app_id):
        claims = get_jwt_claims()
        if claims["type"] != "admin":
            return {"message": "access denied"}

        app = AppointmentModel.find_by_id(app_id)
        if not app:
            return {"message": "Appointment not found"}, 404
        app.delete_from_db()
        return {"message": "Appointment deleted"}
