import os
import sqlite3

# Single source of truth for the database file location
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lostandfound.db')


def get_connection():
    """Open a connection with row access by column name (row['category'])."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table — columns match the signup/login forms
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  TEXT UNIQUE NOT NULL,
            name     TEXT NOT NULL,
            email    TEXT NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL
        )
    ''')

    # 2. Items Table — columns match the "Found an Item" finder form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category    TEXT,
            description TEXT,
            identifier  TEXT,
            location    TEXT,
            date        TEXT,
            contact     TEXT,
            image_path  TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Claims Table — columns match the ownership-claim form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claimed_item     TEXT,
            proof_identifier TEXT,
            contact          TEXT,
            status           TEXT DEFAULT 'Pending Verification',
            created_at       TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed the master security account used for testing (only once)
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", ("123456789",))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
            ("123456789", "Admin Officer", "security@usiu.ac.ke", "password123", "security"),
        )

    conn.commit()
    conn.close()
    print("Database and tables initialized successfully!")


if __name__ == '__main__':
    init_db()
