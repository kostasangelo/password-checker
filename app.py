from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling

def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          email TEXT UNIQUE NOT NULL,
                          username TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL)''')
        conn.commit()

init_db()

def password_strength(user_input):
    has_upper = any(c.isupper() for c in user_input)
    has_lower = any(c.islower() for c in user_input)
    has_digit = any(c.isdigit() for c in user_input)
    has_symbols = any(c in '!@#$%^&*"£' for c in user_input)

    if len(user_input) < 8:
        return 'Password is too short! Must be at least 8 characters.'
    if not has_upper:
        return 'Password must contain at least 1 uppercase letter'
    if not has_lower:
        return 'Password must contain at least 1 lowercase letter'
    if not has_digit:
        return 'Password must contain digits'
    if not has_symbols:
        return 'Password must contain at least 1 special character'

    return 'Your password is strong!' if has_upper and has_lower and has_digit and has_symbols else 'Your password is weak!'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['password']
        result = password_strength(user_input)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                               (email, username, hashed_pw))
                conn.commit()
                return redirect(url_for('index'))  # Redirect to login page
            except sqlite3.IntegrityError:
                return "Username or Email already exists!"

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']}!"
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
