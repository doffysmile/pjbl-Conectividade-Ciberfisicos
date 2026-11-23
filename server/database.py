
import sqlite3
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "smartspace.db")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize():
    print(f"Initializing database at: {DATABASE_PATH}")

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            temperature REAL,
            occupancy INTEGER,
            timestamp REAL
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully!")


def save_measurement(room, data):
    conn = get_connection()

    conn.execute("""
        INSERT INTO measurements
        (room, temperature, occupancy, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        room,
        data["temperature"],
        data["occupancy"],
        data["timestamp"]
    ))

    conn.commit()
    conn.close()

def consult_measurement():
    conn = get_connection()

    conn.execute("""
        SELECT * FROM measurements
    """)

    for row in conn.fetchall():
        print(row)

    conn.commit()
    conn.close()
