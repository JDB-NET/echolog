import os
import pytz
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from datetime import date as datedate
from datetime import datetime as dt
import mysql.connector
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

TIMEZONE = os.getenv('TZ', 'UTC')
tz = pytz.timezone(TIMEZONE)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecret')
app.config['LOGIN_ENABLED'] = os.getenv('LOGIN_ENABLED', 'false').lower() == 'true'

mysql_config = {
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DATABASE', 'echolog')
}

def get_db_connection():
    return mysql.connector.connect(**mysql_config)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal_entry (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        content TEXT NOT NULL
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 7
    offset = (page - 1) * per_page
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SQL_CALC_FOUND_ROWS * FROM journal_entry ORDER BY date DESC LIMIT %s OFFSET %s", (per_page, offset))
    entries = cursor.fetchall()
    cursor.execute("SELECT FOUND_ROWS() as total")
    total = cursor.fetchone()['total']
    cursor.close()
    conn.close()
    has_prev = page > 1
    has_next = offset + per_page < total
    today = datetime.now(tz).date().isoformat()
    now = datetime.now(tz)
    return render_template('index.html', entries=entries, today=today, page=page, has_prev=has_prev, has_next=has_next, now=now)

@app.route('/add', methods=['POST'])
def add_entry():
    date = request.form.get('date', datetime.now(tz).strftime('%Y-%m-%d'))
    content = request.form.get('content', '')
    if content.strip():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journal_entry (date, content) VALUES (%s, %s)", (date, content))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    date = request.args.get('date', None)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM journal_entry WHERE 1=1"
    params = []
    if query:
        sql += " AND content LIKE %s"
        params.append(f"%{query}%")
    if date:
        sql += " AND date = %s"
        params.append(date)
    sql += " ORDER BY date DESC"
    cursor.execute(sql, params)
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    today = datetime.now(tz).date().isoformat()
    now = datetime.now(tz)
    page = 1
    has_prev = False
    has_next = False
    return render_template('index.html', entries=entries, today=today, now=now, page=page, has_prev=has_prev, has_next=has_next)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not app.config['LOGIN_ENABLED']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == os.getenv('LOGIN_USERNAME', 'admin') and password == os.getenv('LOGIN_PASSWORD', 'admin'):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.before_request
def require_login():
    if app.config['LOGIN_ENABLED'] and not session.get('logged_in') and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        date = request.form.get('date')
        content = request.form.get('content')
        cursor.execute("UPDATE journal_entry SET date=%s, content=%s WHERE id=%s", (date, content, entry_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM journal_entry WHERE id=%s", (entry_id,))
        entry = cursor.fetchone()
        cursor.close()
        conn.close()
        if not entry:
            return redirect(url_for('index'))
        return render_template('edit.html', entry=entry)

@app.route('/edit_modal', methods=['POST'])
def edit_entry_modal():
    entry_id = request.form.get('id')
    date = request.form.get('date')
    content = request.form.get('content')
    if entry_id and date and content:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE journal_entry SET date=%s, content=%s WHERE id=%s", (date, content, entry_id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM journal_entry WHERE id=%s", (entry_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)