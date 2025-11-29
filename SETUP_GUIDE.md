# Backend Jobs System - Quick Setup Guide

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Email (Gmail Example)

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your Gmail credentials:**
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=hospital@cardiology-dept.com
   ```

3. **For Gmail, get your App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated password
   - Paste it as `MAIL_PASSWORD` in `.env`

### Step 3: Start the Backend

```bash
python app.py
```

You should see:
```
============================================================
🏥 HOSPITAL INFORMATION SYSTEM - CARDIOLOGY DEPARTMENT
============================================================
✓ Email service initialized
✓ Scheduler initialized with 3 jobs:
  - Daily reminders at 08:00
  - Monthly reports on 1st at 09:00
  - Cleanup expired exports at 02:00
============================================================
```

---

## 📋 System Features

### 1. Daily Appointment Reminders ⏰
- **When:** Every day at 8:00 AM
- **Who:** Patients with appointments tomorrow
- **What:** Email reminder with appointment details

### 2. Monthly Activity Reports 📊
- **When:** 1st of every month at 9:00 AM
- **Who:** All doctors
- **What:** HTML email report with monthly statistics and appointment details

### 3. Treatment History Export 📥
- **When:** Patient-triggered (on demand)
- **Who:** Patients
- **What:** CSV file with all treatment history
- **Access:** Via `/exporthistory` route in patient dashboard

---

## 🗂️ File Structure

New files created:

```
backend/
├── models/
│   ├── email_helper.py              ✨ Email utilities
│   ├── treatment_export.py          ✨ Export database model
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── scheduler.py             ✨ APScheduler config
│   │   └── tasks.py                 ✨ Job implementations
│   └── resources/
│       └── export.py                ✨ Export API endpoints
├── .env.example                     ✨ Email config template
├── .env                             ⚙️ Your email credentials
├── JOBS_DOCUMENTATION.md            📖 Detailed documentation
└── app.py                           ✏️ Updated with jobs init

frontend/
├── src/
│   ├── components/
│   │   └── pages/patient/
│   │       └── ExportTreatmentHistory.vue    ✨ New export page
│   └── router.js                    ✏️ Updated with export route
```

---

## 🔧 Customizing Job Times

Edit `app.py` in the `if __name__ == "__main__":` section:

```python
# Change daily reminder time to 10 AM
add_daily_reminder_job(send_daily_reminders, hour=10, minute=0)

# Change monthly report to 15th at 8 AM
add_monthly_report_job(send_monthly_reports, day=15, hour=8, minute=0)

# Change cleanup to 3 AM
add_cleanup_job(cleanup_expired_exports, hour=3, minute=0)
```

---

## 🧪 Testing

### Test Email Configuration

```bash
# In Python shell
from models.email_helper import send_test_email
send_test_email('your-email@example.com')
```

### Check Scheduled Jobs

```bash
# In Python shell
from models.jobs.scheduler import get_jobs
jobs = get_jobs()
for job in jobs:
    print(f"{job.name} - Next run: {job.next_run_time}")
```

---

## 📱 Patient Export Dashboard

### Access the Export Feature
1. Login as patient
2. Go to Patient Home
3. Click "Export Treatment History" card
4. Click "Export as CSV" button
5. Status updates automatically
6. Download when complete (expires in 7 days)

### What's Included in Export
- Patient ID and Name
- Consulting Doctor Information
- Doctor's Specialization
- Appointment Dates
- Diagnosis Given
- Treatment/Prescription Details
- Follow-up Recommendations

---

## 🔍 Monitoring Jobs

### Console Output

Jobs print detailed status to console:

```
============================================================
📅 DAILY REMINDER JOB STARTED
============================================================
📋 Found 2 appointment(s) for 2024-01-16
✓ Appointment reminder sent to patient1@gmail.com
✓ Appointment reminder sent to patient2@gmail.com
✅ 2 reminder(s) sent successfully
============================================================
```

### Database Tracking

All exports are tracked in `TreatmentExports` table:
- Export status (pending → processing → completed)
- Creation and completion timestamps
- Expiration date (7 days from creation)
- Error messages (if failed)

---

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'apscheduler'"
**Solution:** Install requirements again
```bash
pip install -r requirements.txt
```

### Emails not sending
**Solution:** Verify `.env` file exists and has correct credentials
```bash
# Check if .env exists
ls -la .env

# For Gmail, test App Password
# Ensure you're using the 16-character App Password, not your account password
```

### "RuntimeError: Working outside of application context"
**Solution:** Don't manually call job functions. Let the scheduler run them automatically.

### Export folder permission denied
**Solution:** Create the directory manually
```bash
mkdir -p static/exports
chmod 755 static/exports
```

---

## 📖 Full Documentation

See `JOBS_DOCUMENTATION.md` for:
- Detailed API endpoint documentation
- Job specifications and scheduling details
- Email configuration options
- Database schema
- Future enhancement ideas

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Configure email with `.env` file
3. ✅ Start Flask backend
4. ✅ Start Vue frontend
5. ✅ Test daily reminders (check logs)
6. ✅ Test patient export feature
7. ✅ Test monthly reports (or manually trigger)

**The system is now ready with automated jobs!** 🎉
