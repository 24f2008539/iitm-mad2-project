"""
Job Tasks - Business logic for scheduled jobs
"""
from datetime import datetime, timedelta
from models.appointment import AppointmentModel
from models.patient import PatientModel
from models.doctor import DoctorModel
from models.examination import ExaminationModel
from models.treatment_export import TreatmentExportModel
from models.email_helper import (
    send_appointment_reminder,
    send_monthly_report,
    send_export_notification
)
import csv
import os
from flask import current_app


def send_daily_reminders():
    """
    Daily Job: Check for appointments tomorrow and send reminders
    Runs every morning at 8 AM
    """
    try:
        print("\n" + "="*60)
        print("📅 DAILY REMINDER JOB STARTED")
        print("="*60)
        
        # Get tomorrow's date
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        
        # Find all appointments for tomorrow
        appointments = AppointmentModel.find_by_date(tomorrow)
        
        if not appointments:
            print(f"ℹ️ No appointments scheduled for {tomorrow}")
            print("="*60 + "\n")
            return
        
        print(f"📋 Found {len(appointments)} appointment(s) for {tomorrow}")
        
        # Send reminders to each patient
        reminder_count = 0
        for appointment in appointments:
            if appointment.patient and appointment.doctor:
                patient = appointment.patient
                doctor = appointment.doctor
                
                success = send_appointment_reminder(
                    patient_email=patient.email,
                    patient_name=f"{patient.first_name} {patient.last_name}",
                    appointment_date=appointment.date.strftime("%A, %B %d, %Y"),
                    doctor_name=f"Dr. {doctor.first_name} {doctor.last_name}",
                    appointment_time="09:00 AM"  # Can be customized
                )
                
                if success:
                    reminder_count += 1
        
        print(f"✅ {reminder_count} reminder(s) sent successfully")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ ERROR in daily reminder job: {str(e)}")
        print("="*60 + "\n")


def send_monthly_reports():
    """
    Monthly Job: Generate and send activity reports to all doctors
    Runs on the 1st of every month at 9 AM
    """
    try:
        print("\n" + "="*60)
        print("📊 MONTHLY REPORT JOB STARTED")
        print("="*60)
        
        # Get all doctors
        doctors = DoctorModel.query.all()
        
        if not doctors:
            print("ℹ️ No doctors found")
            print("="*60 + "\n")
            return
        
        print(f"📋 Generating reports for {len(doctors)} doctor(s)")
        
        # Get current month and year
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        
        report_count = 0
        
        # Generate report for each doctor
        for doctor in doctors:
            # Get doctor's appointments for the month
            appointments = AppointmentModel.query.filter(
                AppointmentModel.doctor_id == doctor.id,
                AppointmentModel.date.between(month_start.date(), month_end.date())
            ).all()
            
            if not appointments:
                print(f"  ℹ️ Dr. {doctor.first_name} {doctor.last_name}: No appointments this month")
                continue
            
            # Get examinations for those appointments
            examination_data = []
            for appointment in appointments:
                examinations = ExaminationModel.query.filter_by(
                    appointment_id=appointment.id
                ).all()
                examination_data.extend(examinations)
            
            # Generate HTML report
            report_html = generate_doctor_report_html(
                doctor=doctor,
                appointments=appointments,
                examinations=examination_data,
                month=now.strftime("%B %Y")
            )
            
            # Send report
            success = send_monthly_report(
                doctor_email=doctor.email,
                doctor_name=f"Dr. {doctor.first_name} {doctor.last_name}",
                report_html=report_html
            )
            
            if success:
                report_count += 1
        
        print(f"✅ {report_count} report(s) sent successfully")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ ERROR in monthly report job: {str(e)}")
        print("="*60 + "\n")


def cleanup_expired_exports():
    """
    Daily Job: Clean up expired CSV exports (older than 7 days)
    Runs daily at 2 AM
    """
    try:
        print("\n" + "="*60)
        print("🧹 CLEANUP JOB STARTED")
        print("="*60)
        
        count = TreatmentExportModel.cleanup_expired()
        
        if count > 0:
            print(f"🗑️ Deleted {count} expired export(s)")
        else:
            print("ℹ️ No expired exports to clean up")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ ERROR in cleanup job: {str(e)}")
        print("="*60 + "\n")


def generate_doctor_report_html(doctor, appointments, examinations, month):
    """Generate HTML report for doctor's monthly activity"""
    
    appointment_rows = ""
    for appointment in appointments:
        exam_info = "N/A"
        for exam in examinations:
            if exam.appointment_id == appointment.id:
                exam_info = f"Diagnosis: {exam.diagnosis[:50]}..."
                break
        
        appointment_rows += f"""
        <tr>
            <td>{appointment.date.strftime("%Y-%m-%d")}</td>
            <td>{appointment.patient.first_name} {appointment.patient.last_name}</td>
            <td>{exam_info}</td>
        </tr>
        """
    
    total_appointments = len(appointments)
    total_examinations = len(examinations)
    
    html_report = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #1976d2; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f5f5f5; font-weight: bold; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Monthly Activity Report</h1>
                <p>Dr. {doctor.first_name} {doctor.last_name}</p>
                <p>Specialization: {doctor.specialization}</p>
                <p>Month: {month}</p>
            </div>
            
            <div class="section">
                <h2>Summary Statistics</h2>
                <table>
                    <tr>
                        <td><strong>Total Appointments:</strong></td>
                        <td>{total_appointments}</td>
                    </tr>
                    <tr>
                        <td><strong>Examinations Conducted:</strong></td>
                        <td>{total_examinations}</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>Appointment Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Patient</th>
                            <th>Examination Info</th>
                        </tr>
                    </thead>
                    <tbody>
                        {appointment_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p>This is an automated report generated by the Hospital Information System.</p>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </body>
    </html>
    """
    
    return html_report


def generate_patient_csv_export(patient_id):
    """
    Generate CSV file with patient's treatment history
    This is called by the async export job
    """
    try:
        print(f"\n📄 Generating CSV for patient {patient_id}...")
        
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            raise Exception(f"Patient {patient_id} not found")
        
        # Get all examinations for patient (which include appointments)
        examinations = ExaminationModel.find_all_filtered(patient_id)
        
        # Create CSV file
        csv_filename = f"patient_{patient_id}_treatment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/exports'), csv_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Write CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Patient ID',
                'Patient Name',
                'Doctor Name',
                'Doctor Specialization',
                'Appointment Date',
                'Diagnosis',
                'Treatment/Prescription',
                'Next Visit'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for exam in examinations:
                writer.writerow({
                    'Patient ID': patient.id,
                    'Patient Name': f"{patient.first_name} {patient.last_name}",
                    'Doctor Name': f"Dr. {exam.appointment.doctor.first_name} {exam.appointment.doctor.last_name}" if exam.appointment and exam.appointment.doctor else 'N/A',
                    'Doctor Specialization': exam.appointment.doctor.specialization if exam.appointment and exam.appointment.doctor else 'N/A',
                    'Appointment Date': exam.appointment.date.strftime("%Y-%m-%d") if exam.appointment else 'N/A',
                    'Diagnosis': exam.diagnosis or 'N/A',
                    'Treatment/Prescription': exam.prescription or 'N/A',
                    'Next Visit': 'As per doctor recommendation'  # Can be enhanced with follow-up appointments
                })
        
        print(f"✅ CSV generated successfully at: {csv_path}")
        return csv_path
        
    except Exception as e:
        print(f"❌ ERROR generating CSV: {str(e)}")
        raise


def process_pending_exports():
    """
    Process pending exports (can be called periodically)
    """
    try:
        pending_exports = TreatmentExportModel.find_pending()
        
        for export in pending_exports:
            export.mark_processing()
            
            try:
                # Generate the export
                file_path = generate_patient_csv_export(export.patient_id)
                export.mark_completed(file_path)
                
                # Send notification to patient
                patient = PatientModel.find_by_id(export.patient_id)
                download_link = f"http://localhost:5000/download/export/{export.id}"
                
                send_export_notification(
                    patient_email=patient.email,
                    patient_name=f"{patient.first_name} {patient.last_name}",
                    download_link=download_link,
                    export_type="CSV"
                )
                
            except Exception as e:
                export.mark_failed(str(e))
                
    except Exception as e:
        print(f"❌ ERROR processing exports: {str(e)}")
