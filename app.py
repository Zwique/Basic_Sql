from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Add a sample user
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'supersecurepassword')")
    conn.commit()
    conn.close()

# Vulnerable login function
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Vulnerable SQL query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Login successful! The flag is: " + open('flag.txt').read()
        else:
            return "Invalid credentials!"
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)