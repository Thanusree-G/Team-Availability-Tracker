from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect('team.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    available INTEGER
)
''')

# Insert sample users
users = [
    (1, 'Rakshan', 1),
    (2, 'Rahul', 0),
    (3, 'Sneha', 1)
]

for user in users:
    cursor.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', user)

conn.commit()
conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('team.db')
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    return render_template('index.html', users=users)

@app.route('/toggle/<int:id>')
def toggle(id):
    conn = sqlite3.connect('team.db')

    current = conn.execute(
        'SELECT available FROM users WHERE id=?',
        (id,)
    ).fetchone()[0]

    new_value = 0 if current == 1 else 1

    conn.execute(
        'UPDATE users SET available=? WHERE id=?',
        (new_value, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)