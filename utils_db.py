# utils_db.py
import sqlite3
from datetime import datetime

DB_PATH = "patients.db"

# ------------------------- CONNECTION -------------------------
def connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ------------------------- PATIENT ----------------------------
def add_or_get_patient(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patients WHERE name = ?", (name,))
    result = cursor.fetchone()
    if result:
        patient_id = result[0]
    else:
        cursor.execute("INSERT INTO patients (name) VALUES (?)", (name,))
        conn.commit()
        patient_id = cursor.lastrowid
    conn.close()
    return patient_id


def get_all_patient_names():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM patients ORDER BY name ASC")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

# ------------------------- RECORDS ----------------------------
def save_prediction(patient_id, image_path, predicted_class, confidence):
    conn = connect()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO records (patient_id, image_path, predicted_class, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, image_path, predicted_class, confidence, timestamp))
    conn.commit()
    conn.close()


def get_records_by_patient(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.image_path, r.predicted_class, r.confidence, r.timestamp
        FROM records r
        JOIN patients p ON r.patient_id = p.id
        WHERE p.name = ?
        ORDER BY r.timestamp DESC
    """, (name,))
    results = cursor.fetchall()
    conn.close()
    return results


def get_records_by_date(date_str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, r.image_path, r.predicted_class, r.confidence, r.timestamp
        FROM records r
        JOIN patients p ON r.patient_id = p.id
        WHERE DATE(r.timestamp) = ?
        ORDER BY r.timestamp DESC
    """, (date_str,))
    results = cursor.fetchall()
    conn.close()
    return results
