# ------------------- Imports & Configurations -------------------

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from flask_caching import Cache
import datetime
import threading
import csv
from io import StringIO

# Flask app setup
app = Flask(__name__)
app.secret_key = 'quizmaster_secret'

# ---- Mail (SendGrid SMTP) config ----
app.config.update(
    MAIL_SERVER='smtp.sendgrid.net',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='apikey',
    MAIL_PASSWORD='ACV1JHkGsR8mY',
    MAIL_DEFAULT_SENDER='jishnutejad@gmail.com'
)
mail = Mail(app)

# ---- Caching: simple in-memory ----
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# ---- Scheduler for background jobs ----
scheduler = BackgroundScheduler()
scheduler.start()

# ---- DB configuration ----
db_file = 'quiz.db'


# ------------------- Database Utilities -------------------

def get_db_connection():
    """Create SQLite connection with dict row factory."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create DB tables if not present and insert default values."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                qualification TEXT NOT NULL,
                dob TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                email TEXT,
                last_login DATETIME
            )
        ''')

        # Subjects
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        # Chapters
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
        ''')

        # Quizzes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                chapter_id INTEGER NOT NULL,
                FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
                FOREIGN KEY(chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
            )
        ''')

        # Questions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                option3 TEXT NOT NULL,
                option4 TEXT NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
            )
        ''')

        # Settings (quiz duration)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_duration INTEGER NOT NULL
            )
        ''')

        # Scores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                quiz_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE SET NULL
            )
        ''')

        # Default admin and settings insert if missing
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
        if cursor.fetchone()[0] == 0:
            hashed_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (username, password, full_name, qualification, dob, role, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', hashed_password, 'Administrator', 'N/A', '2000-01-01', 'admin', 'admin@example.com'))

        cursor.execute("SELECT COUNT(*) FROM settings")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO settings (quiz_duration) VALUES (?)", (60,))

        conn.commit()
init_db()


# ------------------- Decorators -------------------

def login_required(f):
    """Require login for access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require admin login for access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            flash('Admin login required.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """Require regular user login for access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'user':
            flash('User login required.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------- Admin Routes -------------------

@app.route('/admin')
@admin_required
def admin():
    """Admin dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quiz_duration FROM settings ORDER BY id DESC LIMIT 1")
    duration = cursor.fetchone()
    duration_val = duration['quiz_duration'] if duration else 60
    conn.close()
    return render_template('admin.html', duration=duration_val)

@app.route('/admin/update_duration', methods=['POST'])
@admin_required
def update_duration():
    """Update quiz duration (admin)."""
    try:
        new_duration = int(request.form.get('quiz_duration'))
    except:
        flash('Invalid quiz duration', 'danger')
        return redirect(url_for('admin'))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM settings")
        cursor.execute("INSERT INTO settings (quiz_duration) VALUES (?)", (new_duration,))
        conn.commit()
    flash('Quiz duration updated!', 'success')
    return redirect(url_for('admin'))

# ----- Subjects -----
@app.route('/admin/subjects', methods=['GET', 'POST'])
@admin_required
def manage_subjects():
    """Add, search, and list subjects."""
    conn = get_db_connection()
    cursor = conn.cursor()
    search_query = request.args.get('search', '').strip()

    if request.method == 'POST':
        name = request.form['subject_name'].strip()
        if name:
            try:
                cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
                conn.commit()
                flash('Subject added successfully', 'success')
            except sqlite3.IntegrityError:
                flash('Subject name already exists', 'danger')
        else:
            flash('Subject name cannot be empty', 'danger')
        return redirect(url_for('manage_subjects'))

    if search_query:
        subjects = cursor.execute("SELECT * FROM subjects WHERE name LIKE ?", ('%' + search_query + '%',)).fetchall()
    else:
        subjects = cursor.execute("SELECT * FROM subjects").fetchall()
    conn.close()
    return render_template('manage_subjects.html', subjects=subjects, search_query=search_query)

@app.route('/admin/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
@admin_required
def edit_subject(subject_id):
    """Edit a subject."""
    conn = get_db_connection()
    cursor = conn.cursor()
    subject = cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    if not subject:
        flash('Subject not found', 'danger')
        return redirect(url_for('manage_subjects'))
    if request.method == 'POST':
        new_name = request.form['subject_name'].strip()
        if new_name:
            try:
                cursor.execute("UPDATE subjects SET name = ? WHERE id = ?", (new_name, subject_id))
                conn.commit()
                flash('Subject updated successfully', 'success')
                return redirect(url_for('manage_subjects'))
            except sqlite3.IntegrityError:
                flash('Subject name already exists', 'danger')
        else:
            flash('Subject name cannot be empty', 'danger')
    conn.close()
    return render_template('edit_subject.html', subject=subject)

@app.route('/admin/delete_subject/<int:subject_id>')
@admin_required
def delete_subject(subject_id):
    """Delete a subject."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        conn.commit()
    flash('Subject deleted successfully', 'danger')
    return redirect(url_for('manage_subjects'))

# ----- Chapters -----
@app.route('/admin/chapters/<int:subject_id>', methods=['GET', 'POST'])
@admin_required
def manage_chapters(subject_id):
    """Add, search, and list chapters in a subject."""
    conn = get_db_connection()
    cursor = conn.cursor()
    subject = cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,)).fetchone()
    if not subject:
        flash('Subject not found', 'danger')
        conn.close()
        return redirect(url_for('manage_subjects'))

    search_query = request.args.get('search', '').strip()

    if request.method == 'POST':
        name = request.form['chapter_name'].strip()
        if name:
            cursor.execute("INSERT INTO chapters (subject_id, name) VALUES (?, ?)", (subject_id, name))
            conn.commit()
            flash('Chapter added successfully', 'success')
            return redirect(url_for('manage_chapters', subject_id=subject_id))
        else:
            flash('Chapter name cannot be empty', 'danger')

    if search_query:
        chapters = cursor.execute(
            "SELECT * FROM chapters WHERE subject_id = ? AND name LIKE ?", (subject_id, '%' + search_query + '%')).fetchall()
    else:
        chapters = cursor.execute("SELECT * FROM chapters WHERE subject_id = ?", (subject_id,)).fetchall()
    conn.close()
    return render_template('manage_chapters.html', chapters=chapters, subject=subject, search_query=search_query)

@app.route('/admin/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
@admin_required
def edit_chapter(chapter_id):
    """Edit a chapter."""
    conn = get_db_connection()
    cursor = conn.cursor()
    chapter = cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
    if not chapter:
        flash('Chapter not found', 'danger')
        return redirect(url_for('manage_subjects'))
    if request.method == 'POST':
        new_name = request.form['chapter_name'].strip()
        if new_name:
            cursor.execute("UPDATE chapters SET name = ? WHERE id = ?", (new_name, chapter_id))
            conn.commit()
            flash('Chapter updated successfully', 'success')
            return redirect(url_for('manage_chapters', subject_id=chapter['subject_id']))
        else:
            flash('Chapter name cannot be empty', 'danger')
    conn.close()
    return render_template('edit_chapter.html', chapter=chapter)

@app.route('/admin/delete_chapter/<int:chapter_id>')
@admin_required
def delete_chapter(chapter_id):
    """Delete a chapter."""
    with get_db_connection() as conn:
        subject_row = conn.execute("SELECT subject_id FROM chapters WHERE id = ?", (chapter_id,)).fetchone()
        subject_id = subject_row['subject_id'] if subject_row else None
        conn.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
        conn.commit()
    flash('Chapter deleted successfully', 'danger')
    if subject_id:
        return redirect(url_for('manage_chapters', subject_id=subject_id))
    else:
        return redirect(url_for('manage_subjects'))

# ----- Quizzes -----
@app.route('/admin/quizzes/<int:chapter_id>', methods=['GET', 'POST'])
@admin_required
def manage_quizzes(chapter_id):
    """Add, search, and list quizzes in a chapter."""
    conn = get_db_connection()
    chapter = conn.execute('SELECT * FROM chapters WHERE id = ?', (chapter_id,)).fetchone()
    if not chapter:
        flash('Chapter not found', 'danger')
        conn.close()
        return redirect(url_for('manage_subjects'))

    search_query = request.args.get('search', '').strip()

    if request.method == 'POST':
        quiz_name = request.form['quiz_name'].strip()
        if quiz_name:
            subject_id = chapter['subject_id']
            conn.execute("INSERT INTO quizzes (name, subject_id, chapter_id) VALUES (?, ?, ?)",
                         (quiz_name, subject_id, chapter_id))
            conn.commit()
            flash('Quiz created successfully', 'success')
            return redirect(url_for('manage_quizzes', chapter_id=chapter_id))
        else:
            flash('Quiz name cannot be empty', 'danger')

    if search_query:
        quizzes = conn.execute(
            "SELECT * FROM quizzes WHERE chapter_id = ? AND name LIKE ?", (chapter_id, '%' + search_query + '%')).fetchall()
    else:
        quizzes = conn.execute("SELECT * FROM quizzes WHERE chapter_id = ?", (chapter_id,)).fetchall()
    conn.close()
    return render_template('manage_quizzes.html', quizzes=quizzes, chapter=chapter, search_query=search_query)

@app.route('/admin/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
def edit_quiz(quiz_id):
    """Edit a quiz."""
    conn = get_db_connection()
    cursor = conn.cursor()
    quiz = cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    if not quiz:
        flash('Quiz not found', 'danger')
        return redirect(url_for('manage_subjects'))
    if request.method == 'POST':
        new_name = request.form['quiz_name'].strip()
        if new_name:
            cursor.execute("UPDATE quizzes SET name = ? WHERE id = ?", (new_name, quiz_id))
            conn.commit()
            flash('Quiz updated successfully', 'success')
            return redirect(url_for('manage_quizzes', chapter_id=quiz['chapter_id']))
        else:
            flash('Quiz name cannot be empty', 'danger')
    conn.close()
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/admin/delete_quiz/<int:quiz_id>')
@admin_required
def delete_quiz(quiz_id):
    """Delete a quiz."""
    with get_db_connection() as conn:
        quiz_row = conn.execute("SELECT chapter_id FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
        if quiz_row is None:
            flash('Quiz not found.', 'danger')
            return redirect(url_for('manage_subjects'))
        chapter_id = quiz_row['chapter_id']
        conn.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        conn.commit()
    flash('Quiz deleted successfully', 'danger')
    return redirect(url_for('manage_quizzes', chapter_id=chapter_id))

# ----- Questions -----
@app.route('/admin/quiz_questions/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
def manage_questions(quiz_id):
    """Add and list questions for a quiz."""
    conn = get_db_connection()
    quiz = conn.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    if not quiz:
        flash('Quiz not found', 'danger')
        conn.close()
        return redirect(url_for('manage_subjects'))

    if request.method == 'POST':
        question = request.form['question'].strip()
        option1 = request.form['option1'].strip()
        option2 = request.form['option2'].strip()
        option3 = request.form['option3'].strip()
        option4 = request.form['option4'].strip()
        answer = request.form['answer'].strip()

        if all([question, option1, option2, option3, option4, answer]):
            if answer not in {option1, option2, option3, option4}:
                flash('Correct answer must match one of the options.', 'danger')
            else:
                conn.execute(
                    "INSERT INTO questions (quiz_id, question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (quiz_id, question, option1, option2, option3, option4, answer)
                )
                conn.commit()
                flash('Question added successfully', 'success')
        else:
            flash('All fields are required to add a question', 'danger')

    questions = conn.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()
    conn.close()
    return render_template('manage_questions.html', questions=questions, quiz=quiz)

@app.route('/admin/edit_question/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    """Edit a question."""
    conn = get_db_connection()
    cursor = conn.cursor()
    question = cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
    if not question:
        flash('Question not found.', 'danger')
        return redirect(url_for('manage_subjects'))
    if request.method == 'POST':
        q_text = request.form['question'].strip()
        o1 = request.form['option1'].strip()
        o2 = request.form['option2'].strip()
        o3 = request.form['option3'].strip()
        o4 = request.form['option4'].strip()
        ans = request.form['answer'].strip()

        if all([q_text, o1, o2, o3, o4, ans]):
            if ans not in {o1, o2, o3, o4}:
                flash('Correct answer must be one of the options', 'danger')
            else:
                cursor.execute('''
                    UPDATE questions SET question=?, option1=?, option2=?, option3=?, option4=?, answer=?
                    WHERE id = ?
                ''', (q_text, o1, o2, o3, o4, ans, question_id))
                conn.commit()
                flash('Question updated successfully', 'success')
                return redirect(url_for('manage_questions', quiz_id=question['quiz_id']))
        else:
            flash('All fields are required', 'danger')
    conn.close()
    return render_template('edit_question.html', question=question)

@app.route('/admin/delete_question/<int:question_id>')
@admin_required
def delete_question(question_id):
    """Delete a question."""
    with get_db_connection() as conn:
        question_row = conn.execute("SELECT quiz_id FROM questions WHERE id = ?", (question_id,)).fetchone()
        if question_row is None:
            flash('Question not found.', 'danger')
            return redirect(url_for('manage_subjects'))
        quiz_id = question_row['quiz_id']
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
    flash('Question deleted successfully', 'danger')
    return redirect(url_for('manage_questions', quiz_id=quiz_id))

# ----- Users -----
@app.route('/admin/users', methods=['GET'])
@admin_required
def manage_users():
    """View/search user list."""
    conn = get_db_connection()
    cursor = conn.cursor()
    search_query = request.args.get('search', '').strip()
    if search_query:
        users = cursor.execute(
            "SELECT id, username, full_name, qualification, dob, email FROM users WHERE role='user' AND username LIKE ?",
            ('%' + search_query + '%',)
        ).fetchall()
    else:
        users = cursor.execute("SELECT id, username, full_name, qualification, dob, email FROM users WHERE role='user'").fetchall()
    conn.close()
    return render_template('manage_users.html', users=users, search_query=search_query)

@app.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    """Delete a user account (admin)."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    flash('User deleted successfully', 'danger')
    return redirect(url_for('manage_users'))

# ----- Quiz analytics -----
def get_quiz_performance():
    """Helper: returns user avg scores for analytics."""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, AVG(score) FROM scores GROUP BY username")
        data = cursor.fetchall()
    user_names = [row[0] for row in data]
    user_scores = [row[1] for row in data]
    return user_names, user_scores

@app.route('/admin/analytics')
@admin_required
@cache.cached(timeout=300)
def quiz_analytics():
    """Quiz analytics for admin."""
    user_names, user_scores = get_quiz_performance()
    return render_template('analytics.html', user_names=user_names, user_scores=user_scores)


# ------------------- User Routes -------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            session['role'] = user['role']

            # Update last_login to current UTC time
            with get_db_connection() as conn_update:
                conn_update.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?", (username,))
                conn_update.commit()

            flash(f'Welcome {username}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user_console'))
        else:
            flash('Invalid credentials. Try again or register.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        full_name = request.form['full_name'].strip()
        qualification = request.form['qualification'].strip()
        dob = request.form['dob'].strip()
        email = request.form.get('email', '').strip() or None

        if not all([username, password, full_name, qualification, dob]):
            flash('All fields except email are required.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, qualification, dob, role, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username, hashed_password, full_name, qualification, dob, 'user', email))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/user_console')
@user_required
@cache.cached(timeout=300, key_prefix=lambda: session.get('user'))  # cache per user
def user_console():
    """User main dashboard."""
    username = session['user']
    conn = get_db_connection()
    user = conn.execute("SELECT full_name FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    full_name = user['full_name'] if user else username
    return render_template('user.html', full_name=full_name)

# ----- Quiz selection workflow -----
@app.route('/select_subject', methods=['GET', 'POST'])
@user_required
def select_subject():
    """User selects subject."""
    conn = get_db_connection()
    subjects = conn.execute("SELECT * FROM subjects").fetchall()
    conn.close()
    if request.method == 'POST':
        session['subject_id'] = int(request.form['subject_id'])
        return redirect(url_for('select_chapter'))
    return render_template('select_subject.html', subjects=subjects)

@app.route('/select_chapter', methods=['GET', 'POST'])
@user_required
def select_chapter():
    """User selects chapter in subject."""
    if 'subject_id' not in session:
        return redirect(url_for('select_subject'))
    subject_id = session['subject_id']
    conn = get_db_connection()
    chapters = conn.execute("SELECT * FROM chapters WHERE subject_id = ?", (subject_id,)).fetchall()
    conn.close()
    if request.method == 'POST':
        session['chapter_id'] = int(request.form['chapter_id'])
        return redirect(url_for('select_quiz'))
    return render_template('select_chapter.html', chapters=chapters)

@app.route('/select_quiz', methods=['GET', 'POST'])
@user_required
def select_quiz():
    """User chooses quiz in chapter."""
    if 'chapter_id' not in session:
        return redirect(url_for('select_chapter'))
    chapter_id = session['chapter_id']
    conn = get_db_connection()
    quizzes = conn.execute("SELECT * FROM quizzes WHERE chapter_id = ?", (chapter_id,)).fetchall()
    conn.close()
    if request.method == 'POST':
        session['quiz_id'] = int(request.form['quiz_id'])
        return redirect(url_for('quiz'))
    return render_template('select_quiz.html', quizzes=quizzes)

@app.route('/quiz', methods=['GET', 'POST'])
@user_required
def quiz():
    """User takes a quiz."""
    if 'quiz_id' not in session:
        return redirect(url_for('select_quiz'))
    quiz_id = session['quiz_id']
    conn = get_db_connection()
    questions = conn.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()
    duration_row = conn.execute("SELECT quiz_duration FROM settings ORDER BY id DESC LIMIT 1").fetchone()
    duration = duration_row['quiz_duration'] if duration_row else 60
    if request.method == 'POST':
        form_data = request.form.to_dict()
        score = 0
        total = len(questions)
        for question in questions:
            qid_str = str(question['id'])
            correct_answer = question['answer']
            user_answer = form_data.get(qid_str, "")
            if user_answer == correct_answer:
                score += 1
        conn.execute("INSERT INTO scores (username, quiz_id, score, total) VALUES (?, ?, ?, ?)", (session['user'], quiz_id, score, total))
        conn.commit()
        conn.close()
        return redirect(url_for('view_scores', score=score, total=total))
    conn.close()
    return render_template('quiz.html', questions=questions, duration=duration)

@app.route('/scores')
@user_required
def view_scores():
    """Show user their scores and attempts."""
    score = request.args.get('score', type=int)
    total = request.args.get('total', type=int)
    if score is not None and total is not None:
        return render_template('quiz_results.html', score=score, total=total)

    username = session['user']
    conn = get_db_connection()
    query = '''
        SELECT scores.score, scores.total, scores.timestamp,
               quizzes.name as quiz_name,
               chapters.name as chapter_name,
               subjects.name as subject_name
        FROM scores
        LEFT JOIN quizzes ON scores.quiz_id = quizzes.id
        LEFT JOIN chapters ON quizzes.chapter_id = chapters.id
        LEFT JOIN subjects ON quizzes.subject_id = subjects.id
        WHERE scores.username = ?
        ORDER BY scores.timestamp DESC
    '''
    scores = conn.execute(query, (username,)).fetchall()
    conn.close()
    return render_template('scores.html', scores=scores)


# ------------------- Background Jobs: Email Reminders & Reports -------------------

def send_daily_reminders():
    """Daily: send pending quiz reminders to users by email."""
    with get_db_connection() as conn:
        users = conn.execute("SELECT username, email, last_login FROM users WHERE role = 'user' AND email IS NOT NULL").fetchall()
        quiz_newest = conn.execute("SELECT MAX(id) AS max_id FROM quizzes").fetchone()
        latest_quiz_id = quiz_newest['max_id'] if quiz_newest else 0

        for user in users:
            username = user['username']
            email = 'djishnuteja2006@gmail.com'  # all emails sent here (overriding user emails)
            last_login = user['last_login']
            needs_reminder = False
            if last_login is None:
                needs_reminder = True
            else:
                try:
                    last_login_dt = datetime.datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    last_login_dt = datetime.datetime.utcnow()
                diff = (datetime.datetime.utcnow() - last_login_dt).total_seconds()
                if diff > 24 * 3600:
                    needs_reminder = True

            if needs_reminder:
                try:
                    msg = Message('QuizMaster Daily Reminder', recipients=[email])
                    msg.body = (f"Hello {username},\n\n"
                                "You have pending or new quizzes available. Please visit and attempt them.\n\n"
                                "Best regards,\nQuizMaster Team")
                    mail.send(msg)
                    print(f"Sent daily reminder to {email}")
                except Exception as e:
                    print(f"Failed sending email to {email}, error: {e}")

def send_monthly_reports():
    """Monthly report with user quiz stats (as HTML)."""
    with get_db_connection() as conn:
        users = conn.execute("SELECT username, email FROM users WHERE role='user' AND email IS NOT NULL").fetchall()

        today = datetime.date.today()
        first_day_this_month = today.replace(day=1)
        last_month_last_day = first_day_this_month - datetime.timedelta(days=1)
        last_month_first_day = last_month_last_day.replace(day=1)

        for user in users:
            username = user['username']
            email = 'djishnuteja2006@gmail.com'  # override

            query = '''
                SELECT q.name as quiz_name, COUNT(s.id) as attempts, AVG( CAST(s.score AS FLOAT)/s.total ) as avg_score
                FROM scores s
                JOIN quizzes q ON s.quiz_id = q.id
                WHERE s.username = ? AND s.timestamp BETWEEN ? AND ?
                GROUP BY q.id
            '''
            stats = conn.execute(query, (username, last_month_first_day, last_month_last_day)).fetchall()

            total_attempts = sum(row['attempts'] for row in stats)
            avg_score = 0
            if total_attempts > 0:
                avg_score = sum(row['avg_score'] * row['attempts'] for row in stats) / total_attempts

            html_report = f"<h2>Monthly Quiz Report for {username}</h2>"
            html_report += f"<p>Total Quizzes Attempted: {total_attempts}</p>"
            html_report += f"<p>Average Score: {avg_score:.2%}</p>"
            html_report += "<table border='1' cellpadding='5'><tr><th>Quiz Name</th><th>Attempts</th><th>Avg Score</th></tr>"
            for row in stats:
                html_report += f"<tr><td>{row['quiz_name']}</td><td>{row['attempts']}</td><td>{row['avg_score']:.2%}</td></tr>"
            html_report += "</table>"

            try:
                msg = Message("Your Monthly Quiz Activity Report", recipients=[email])
                msg.html = html_report
                mail.send(msg)
                print(f"Sent monthly report to {email}")
            except Exception as e:
                print(f"Failed sending monthly report to {email}, error: {e}")

# ---- Register scheduled jobs ----
scheduler.add_job(send_daily_reminders, 'cron', hour=18, minute=0)  # 6 PM UTC every day
scheduler.add_job(send_monthly_reports, 'cron', day=1, hour=1, minute=0)  # 1st day of month, 1 AM UTC


# ------------------- User CSV Export (Async Threaded) -------------------

def generate_user_csv(username, email):
    """Generate user's quiz data as CSV and email it (async)."""
    with app.app_context():
        with get_db_connection() as conn:
            query = '''
                SELECT s.quiz_id, q.chapter_id, s.timestamp as date_of_quiz, s.score, s.total,
                       (CASE WHEN s.score >= s.total/2 THEN 'Pass' ELSE 'Fail' END) as remarks
                FROM scores s
                JOIN quizzes q ON s.quiz_id = q.id
                WHERE s.username = ?
            '''
            rows = conn.execute(query, (username,)).fetchall()

        si = StringIO()
        csv_writer = csv.writer(si)
        csv_writer.writerow(['quiz_id', 'chapter_id', 'date_of_quiz', 'score', 'total', 'remarks'])
        for row in rows:
            csv_writer.writerow([row['quiz_id'], row['chapter_id'], row['date_of_quiz'], row['score'], row['total'], row['remarks']])
        csv_content = si.getvalue()
        si.close()

        # Email hardcoded as per requirements
        email = 'djishnuteja2006@gmail.com'

        try:
            msg = Message("Your Quiz Report CSV", recipients=[email])
            msg.body = "Attached is your quiz report CSV."
            msg.attach("quiz_report.csv", "text/csv", csv_content)
            mail.send(msg)
            print(f"Sent CSV export to {email}")
        except Exception as e:
            print(f"Failed sending CSV export email to {email}, error: {e}")

@app.route('/export_user_csv')
@user_required
def export_user_csv():
    """User triggers export of their quiz data as CSV (sent by email)."""
    username = session['user']
    with get_db_connection() as conn:
        user = conn.execute("SELECT email FROM users WHERE username = ?", (username,)).fetchone()
    if not user or not user['email']:
        flash("Email not configured. Cannot send report.", "danger")
        return redirect(url_for('user_console'))

    threading.Thread(target=generate_user_csv, args=(username, user['email'])).start()
    flash("CSV export started. You will receive an email shortly.", "info")
    return redirect(url_for('user_console'))

@app.route('/test_email')
def test_email():
    """Utility: test SMTP sending."""
    try:
        msg = Message("Test Email from QuizMaster", recipients=['djishnuteja2006@gmail.com'])
        msg.body = "This is a test email sent to verify SMTP settings."
        mail.send(msg)
        return "Test email sent successfully! Check your inbox."
    except Exception as e:
        return f"Failed to send: {e}"


# ------------------- Main Entrypoint -------------------

if __name__ == '__main__':
    app.run(debug=True)
