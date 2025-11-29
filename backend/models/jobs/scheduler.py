"""
APScheduler configuration and job scheduling
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import logging

# Configure logging for APScheduler
logging.basicConfig()
scheduler_logger = logging.getLogger('apscheduler.executors.default')
scheduler_logger.setLevel(logging.DEBUG)

# Create global scheduler instance
scheduler = BackgroundScheduler(daemon=True)


def init_scheduler(app):
    """Initialize the scheduler with Flask app"""
    scheduler.start()
    
    # Register shutdown handler
    atexit.register(lambda: scheduler.shutdown())
    
    print("✓ APScheduler initialized and running")
    return scheduler


def add_daily_reminder_job(callback, hour=8, minute=0):
    """
    Add a job that runs daily at specified time (default 8 AM)
    
    Args:
        callback: Function to call for the job
        hour: Hour (0-23)
        minute: Minute (0-59)
    """
    scheduler.add_job(
        callback,
        trigger=CronTrigger(hour=hour, minute=minute),
        id='daily_appointment_reminders',
        name='Daily Appointment Reminders',
        replace_existing=True
    )
    print(f"✓ Daily reminder job scheduled for {hour:02d}:{minute:02d}")


def add_monthly_report_job(callback, day=1, hour=9, minute=0):
    """
    Add a job that runs monthly (default: 1st of month at 9 AM)
    
    Args:
        callback: Function to call for the job
        day: Day of month (1-31)
        hour: Hour (0-23)
        minute: Minute (0-59)
    """
    scheduler.add_job(
        callback,
        trigger=CronTrigger(day=day, hour=hour, minute=minute),
        id='monthly_activity_reports',
        name='Monthly Activity Reports',
        replace_existing=True
    )
    print(f"✓ Monthly report job scheduled for day {day} at {hour:02d}:{minute:02d}")


def add_cleanup_job(callback, hour=2, minute=0):
    """
    Add a job that runs daily to clean up expired exports
    
    Args:
        callback: Function to call for the job
        hour: Hour (0-23)
        minute: Minute (0-59)
    """
    scheduler.add_job(
        callback,
        trigger=CronTrigger(hour=hour, minute=minute),
        id='cleanup_expired_exports',
        name='Cleanup Expired Exports',
        replace_existing=True
    )
    print(f"✓ Cleanup job scheduled for {hour:02d}:{minute:02d}")


def remove_job(job_id):
    """Remove a job by ID"""
    try:
        scheduler.remove_job(job_id)
        print(f"✓ Job {job_id} removed")
        return True
    except Exception as e:
        print(f"✗ Error removing job {job_id}: {str(e)}")
        return False


def get_jobs():
    """Get list of all scheduled jobs"""
    return scheduler.get_jobs()


def pause_scheduler():
    """Pause the scheduler"""
    scheduler.pause()
    print("✓ Scheduler paused")


def resume_scheduler():
    """Resume the scheduler"""
    scheduler.resume()
    print("✓ Scheduler resumed")
