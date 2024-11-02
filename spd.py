from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    with sqlite3.connect('projects.db') as conn:
        c = conn.cursor()
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            profile_image TEXT,
            location TEXT
        )''')
        
        # Resources table
        c.execute('''CREATE TABLE IF NOT EXISTS Resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            images TEXT,
            category TEXT,
            availability TEXT,
            date_posted TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )''')
        
        # Messages table
        c.execute('''CREATE TABLE IF NOT EXISTS Messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            content TEXT NOT NULL,
            timestamp TEXT,
            FOREIGN KEY (sender_id) REFERENCES Users(user_id),
            FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
        )''')
        
        # Reviews table
        c.execute('''CREATE TABLE IF NOT EXISTS Reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reviewer_id INTEGER,
            rating INTEGER,
            comment TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (reviewer_id) REFERENCES Users(user_id)
        )''')

init_db()

@app.route('/')
def index():
    return render_template('index.html')

# User registration
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    
    with sqlite3.connect('projects.db') as conn:
        c = conn.cursor()
        try:
            c.execute('INSERT INTO Users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already exists."
    return redirect(url_for('index'))

# User login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    with sqlite3.connect('projects.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Users WHERE email = ?', (email,))
        user = c.fetchone()
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
    return "Invalid credentials"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# CRUD for resources
@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        images = request.form['images']
        category = request.form['category']
        availability = request.form['availability']
        user_id = session.get('user_id')
        
        with sqlite3.connect('projects.db') as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO Resources (title, description, images, category, availability, user_id) 
                         VALUES (?, ?, ?, ?, ?, ?)''', (title, description, images, category, availability, user_id))
            conn.commit()
        return redirect(url_for('resources'))
    
    # Fetch resources
    with sqlite3.connect('projects.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Resources')
        resources = c.fetchall()
    return render_template('resources.html', resources=resources)

if __name__ == '__main__':
    app.run(debug=True)
