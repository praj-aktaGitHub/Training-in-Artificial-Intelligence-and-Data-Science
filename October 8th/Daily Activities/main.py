from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

employees = [

    {"id": 201, "name": "Aaryan ", "department": "Finance", "salary": 68000.0},
    {"id": 202, "name": "Prajakta", "department": "AI", "salary": 72000.0},
    {"id": 203, "name": "Rohan", "department": "Operations", "salary": 64000.0}
]

@app.get("/employees")
def get_employees():
    return employees

@app.get("/employees")
def get_employee_count():
    total = len(employees)
    return {"total": employees}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for e in employees:
        if e["id"] == employee_id:
            return e
    raise HTTPException(status_code=404, detail="employee not found:(")

@app.post("/employees", status_code=201)
def add_employee(employee : Employee):
    for e in employees:
        if e["id"] == employee.id:
            raise HTTPException(status_code=409, detail="employee already exists:(")
    employees.append(employee.dict())
    return  employee

@app.put("/employees/{employee_id}")
def update_employee(employee_id : int, employee : Employee):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            employees[i] = employee.dict()
            return employee
    raise HTTPException(status_code=404, detail="employee not found:(")

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id : int, employee: Employee):
    for i, e in enumerate(employees):
        if e["id"] == employee_id:
            employees.pop(i)
            return delete_employee
    raise HTTPException(status_code=404, detail="employee not found:(")