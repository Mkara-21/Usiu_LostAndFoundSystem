import sqlite3

def init_db():
    # Connects to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect('usiu_lost_found.db')
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Finder', 'Owner', 'Security'))
        )
    ''')

    # 2. Items Table (As per your strict specifications)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            unique_identifier TEXT NOT NULL,
            last_spotted_location TEXT NOT NULL,
            date_found TEXT NOT NULL,
            image_path TEXT NOT NULL,
            status TEXT DEFAULT 'Pending Security' 
                   CHECK(status IN ('Pending Security', 'Checked-In', 'Claimed'))
        )
    ''')

    # 3. Claims/Verification Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            owner_id TEXT NOT NULL,
            owner_description TEXT NOT NULL,
            owner_identifier TEXT NOT NULL,
            security_status TEXT DEFAULT 'Pending' 
                            CHECK(security_status IN ('Pending', 'Approved', 'Denied')),
            FOREIGN KEY(item_id) REFERENCES items(id),
            FOREIGN KEY(owner_id) REFERENCES users(school_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables initialized successfully!")

if __name__ == '__main__':
    init_db()