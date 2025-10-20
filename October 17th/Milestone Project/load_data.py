import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import get_connection
import csv
from db import TableCreate
TableCreate()
conn = get_connection()
cursor = conn.cursor()

# load patients
with open('data/patients.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
        INSERT IGNORE INTO patients (PatientID, Name, Age, Gender, `Condition`)
        VALUES (%s, %s, %s, %s, %s)
        ''', (row['PatientID'], row['Name'], int(row['Age']), row['Gender'], row['Condition']))

# load doc
with open('data/doctors.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
        INSERT IGNORE INTO doctors (DoctorID, Name, Specialization)
        VALUES (%s, %s, %s)
        ''', (row['DoctorID'], row['Name'], row['Specialization']))

conn.commit()
conn.close()
