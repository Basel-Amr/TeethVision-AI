# init_db.py
import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create the patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

# Create the records table
cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    predicted_class TEXT NOT NULL CHECK(predicted_class IN ('CaS', 'CoS', 'Gum', 'MC', 'OC', 'OLP', 'OT')),
    confidence REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

conn.commit()
conn.close()

print("✅ Database initialized and tables created successfully.")