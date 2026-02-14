import sqlite3
import os

DB_PATH = "storage/smartfit.db"


def get_connection():
    os.makedirs("storage", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identities (
        identity_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        nickname TEXT,
        gender TEXT,
        age INTEGER,
        style_preference TEXT,
        job_type TEXT,
        personality TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clothing_items (
        item_id TEXT PRIMARY KEY,
        identity_id TEXT NOT NULL,
        name TEXT,
        category TEXT,
        color TEXT,
        style TEXT,
        season TEXT,
        raw_image_path TEXT,
        processed_image_path TEXT,
        mask_path TEXT,
        is_processed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(identity_id) REFERENCES identities(identity_id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
