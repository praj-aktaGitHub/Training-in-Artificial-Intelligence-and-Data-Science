from fastapi import APIRouter
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from config.db_config import get_connection

router = APIRouter()

class Doctor(BaseModel):
    DoctorID: str
    Name: str
    Specialization: str

@router.get("/")
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return doctors

@router.post("/")
def add_doctor(doctor: Doctor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctors (DoctorID, Name, Specialization)
        VALUES (%s, %s, %s)
    ''', (doctor.DoctorID, doctor.Name, doctor.Specialization))
    conn.commit()
    conn.close()
    return {"message": "Doctor added successfully"}

@router.put("/{id}")
def update_doctor(id: str, doctor: Doctor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE doctors
        SET Name=%s, Specialization=%s
        WHERE DoctorID=%s
    ''', (doctor.Name, doctor.Specialization, id))
    conn.commit()
    conn.close()
    return {"message": "Doctor updated successfully"}

@router.delete("/{id}")
def delete_doctor(id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE DoctorID=%s", (id,))
    conn.commit()
    conn.close()
    return {"message": "Doctor deleted successfully"}
