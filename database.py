import sqlite3
import json
from datetime import datetime

DB_NAME = "inspection_history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            product_name TEXT,
            status TEXT,
            score REAL,
            result_json TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def convert_numpy(obj):
    """
    Convert NumPy values into normal Python values
    so they can be stored as JSON.
    """

    if hasattr(obj, "item"):
        return obj.item()

    if isinstance(obj, dict):
        return {
            key: convert_numpy(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            convert_numpy(value)
            for value in obj
        ]

    if isinstance(obj, tuple):
        return [
            convert_numpy(value)
            for value in obj
        ]

    return obj


def save_inspection(role, product_name, status, score, result):

    result = convert_numpy(result)

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO inspections
        (role, product_name, status, score, result_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        role,
        product_name,
        status,
        float(score),
        json.dumps(result),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute("""
        SELECT id, role, product_name, status, score, created_at
        FROM inspections
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records