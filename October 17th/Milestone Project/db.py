import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import get_connection

def TableCreate():
    conn = get_connection()
    cursor = conn.cursor()

    # patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        PatientID VARCHAR(10) PRIMARY KEY,
        Name VARCHAR(100),
        Age INT,
        Gender VARCHAR(10),
        `Condition` VARCHAR(100)
    )
    ''')

    # doc table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        DoctorID VARCHAR(10) PRIMARY KEY,
        Name VARCHAR(100),
        Specialization VARCHAR(100)
    )
    ''')

    conn.commit()
    conn.close()
    print('Table created successfully')
