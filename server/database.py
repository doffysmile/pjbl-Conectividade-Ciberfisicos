import sqlite3

def initialize():
    conn = sqlite3.connect("smartspace.db")

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

def save_measurement(room, data):
    conn = sqlite3.connect("smartspace.db")

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