import sqlite3
import config
from pathlib import Path

DB_NAME = config.DATABASE_PATH


def get_connection():
    Path(DB_NAME).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            genre TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_records(table_name):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if table_name not in ["musics"]:
            return None

        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 10")
        data = [dict(row) for row in cursor.fetchall()]
        return data

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_record(name, genre, date, time):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        name = name.strip()
        genre = genre.strip() if genre else None

        cursor.execute(
            """
            INSERT INTO musics (name, genre, date, time)
            VALUES (?, ?, ?, ?)
            """,
            (name, genre, date, time),
        )

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error adding record: {e}")

        if conn:
            conn.rollback()

        return False

    finally:
        if conn:
            conn.close()


def find_record(name):
    """
    بررسی وجود آهنگ در دیتابیس

    Returns:
        bool: True اگر آهنگ وجود داشته باشد
    """

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        name = name.strip()

        cursor.execute(
            """
            SELECT 1
            FROM musics
            WHERE TRIM(name) = ?
            LIMIT 1
            """,
            (name,),
        )

        return cursor.fetchone() is not None

    except sqlite3.Error as e:
        print(f"Error finding record: {e}")
        return False

    finally:
        if conn:
            conn.close()
