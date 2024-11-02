import sqlite3

def init_db():
    with sqlite3.connect('projects.db') as conn:
        c = conn.cursor()
        c.executescript('''
            -- Create Users Table
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                profile_image TEXT,
                location TEXT
            );

            -- Create Resources Table
            CREATE TABLE IF NOT EXISTS Resources (
                resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                images TEXT,
                category TEXT,
                availability TEXT,
                date_posted TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );

            -- Create Messages Table
            CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES Users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
            );

            -- Create Reviews Table
            CREATE TABLE IF NOT EXISTS Reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reviewer_id INTEGER,
                rating INTEGER NOT NULL,
                comment TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (reviewer_id) REFERENCES Users(user_id)
            );
        ''')
        conn.commit()

# Call this function once at the start of your application to set up the database
init_db()
