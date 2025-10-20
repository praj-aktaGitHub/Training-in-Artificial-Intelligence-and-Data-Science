import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

# insert
cursor.execute('''
INSERT INTO patients (PatientID, Name, Age, Gender, `Condition`)
VALUES (%s, %s, %s, %s, %s)
''', ('P009', 'Aaryan', 20, 'Male', 'Migraine'))

# update
cursor.execute('''
UPDATE doctors
SET Specialization = %s
WHERE DoctorID = %s
''', ('Neurologist', 'D101'))

# Delete a patient
cursor.execute('''
DELETE FROM patients
WHERE PatientID = %s
''', ('P002',))

# fetch
cursor.execute('''
SELECT * FROM patients
WHERE Age > 40
''')
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
