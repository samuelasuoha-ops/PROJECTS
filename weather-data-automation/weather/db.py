import os
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS readings (
  ts_utc TEXT PRIMARY KEY,
  temperature_c REAL,
  relative_humidity REAL,
  precipitation_mm REAL
);
"""

def get_conn(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn

def init_db(db_path: str):
    conn = get_conn(db_path)
    with conn:
        conn.executescript(SCHEMA)
    conn.close()

def upsert_readings(db_path: str, rows):
    conn = get_conn(db_path)
    with conn:
        conn.executemany(
            """INSERT INTO readings (ts_utc, temperature_c, relative_humidity, precipitation_mm)
               VALUES (:ts_utc, :temperature_c, :relative_humidity, :precipitation_mm)
               ON CONFLICT(ts_utc) DO UPDATE SET
                    temperature_c=excluded.temperature_c,
                    relative_humidity=excluded.relative_humidity,
                    precipitation_mm=excluded.precipitation_mm
            """,
            rows
        )
    conn.close()
