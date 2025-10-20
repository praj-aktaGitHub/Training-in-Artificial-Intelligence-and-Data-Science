from fastapi import APIRouter
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import get_connection

router = APIRouter()

class Patient(BaseModel):
    PatientID: str
    Name: str
    Age: int
    Gender: str
    Condition: str

@router.get("/")
def get_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return patients

@router.post("/")
def add_patient(patient: Patient):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (PatientID, Name, Age, Gender, `Condition`)
        VALUES (%s, %s, %s, %s, %s)
    ''', (patient.PatientID, patient.Name, patient.Age, patient.Gender, patient.Condition))
    conn.commit()
    conn.close()
    return {"message": "Patient added successfully"}

@router.put("/{id}")
def update_patient(id: str, patient: Patient):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE patients
        SET Name=%s, Age=%s, Gender=%s, `Condition`=%s
        WHERE PatientID=%s
    ''', (patient.Name, patient.Age, patient.Gender, patient.Condition, id))
    conn.commit()
    conn.close()
    return {"message": "Patient updated successfully"}

@router.delete("/{id}")
def delete_patient(id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE PatientID=%s", (id,))
    conn.commit()
    conn.close()
    return {"message": "Patient deleted successfully"}
