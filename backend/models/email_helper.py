"""
Email utility functions for sending reminders, reports, and notifications
"""
import os
from flask import render_template_string
from flask_mail import Mail, Message
from datetime import datetime

# Configuration for Flask-Mail
def configure_email(app):
    """Configure email settings for the Flask app"""
    # You can set these via environment variables or directly here
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'hospital@cardiology-dept.com')
    
    return Mail(app)


mail = None


def init_mail(app):
    """Initialize mail with app"""
    global mail
    mail = configure_email(app)
    return mail


def send_appointment_reminder(patient_email, patient_name, appointment_date, doctor_name, appointment_time="09:00 AM"):
    """Send appointment reminder email to patient"""
    try:
        subject = f"Appointment Reminder - {appointment_date}"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #333;">Appointment Reminder</h2>
                    <p>Dear {patient_name},</p>
                    <p>This is a reminder that you have a scheduled appointment:</p>
                    <table style="margin: 20px 0; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px; font-weight: bold;">Date:</td>
                            <td style="padding: 10px;">{appointment_date}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold;">Time:</td>
                            <td style="padding: 10px;">{appointment_time}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: bold;">Doctor:</td>
                            <td style="padding: 10px;">{doctor_name}</td>
                        </tr>
                    </table>
                    <p>Please ensure you arrive 10 minutes early.</p>
                    <p>Best regards,<br/>Cardiology Department Hospital Information System</p>
                </div>
            </body>
        </html>
        """
        
        msg = Message(subject=subject, recipients=[patient_email], html=html_body)
        mail.send(msg)
        print(f"✓ Appointment reminder sent to {patient_email}")
        return True
    except Exception as e:
        print(f"✗ Error sending appointment reminder: {str(e)}")
        return False


def send_monthly_report(doctor_email, doctor_name, report_html):
    """Send monthly activity report to doctor"""
    try:
        current_month = datetime.now().strftime("%B %Y")
        subject = f"Monthly Activity Report - {current_month}"
        
        msg = Message(subject=subject, recipients=[doctor_email], html=report_html)
        mail.send(msg)
        print(f"✓ Monthly report sent to {doctor_email}")
        return True
    except Exception as e:
        print(f"✗ Error sending monthly report: {str(e)}")
        return False


def send_export_notification(patient_email, patient_name, download_link, export_type="CSV"):
    """Send notification when export is ready"""
    try:
        subject = f"Your {export_type} Export is Ready"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #2e7d32;">Export Ready</h2>
                    <p>Dear {patient_name},</p>
                    <p>Your treatment history {export_type.lower()} export is now ready for download.</p>
                    <p style="margin: 20px 0;">
                        <a href="{download_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
                            Download {export_type}
                        </a>
                    </p>
                    <p style="color: #666; font-size: 12px;">This link is valid for 7 days.</p>
                    <p>Best regards,<br/>Cardiology Department Hospital Information System</p>
                </div>
            </body>
        </html>
        """
        
        msg = Message(subject=subject, recipients=[patient_email], html=html_body)
        mail.send(msg)
        print(f"✓ Export notification sent to {patient_email}")
        return True
    except Exception as e:
        print(f"✗ Error sending export notification: {str(e)}")
        return False


def send_test_email(recipient_email):
    """Send a test email to verify configuration"""
    try:
        subject = "Test Email - Hospital System"
        html_body = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Test Email</h2>
                <p>If you're reading this, the email configuration is working correctly!</p>
                <p>Best regards,<br/>Hospital Information System</p>
            </body>
        </html>
        """
        
        msg = Message(subject=subject, recipients=[recipient_email], html=html_body)
        mail.send(msg)
        print(f"✓ Test email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"✗ Error sending test email: {str(e)}")
        return False
