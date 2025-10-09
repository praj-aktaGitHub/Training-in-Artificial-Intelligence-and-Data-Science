from fastapi.testclient import TestClient
from main import app, Employee

client = TestClient(app)

def test_main():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_employee():
    new_emp = {
        "id": 2,
        "name": "Yash",
        "department": "ML",
        "salary": 10000,
    }
    response = client.post("/employees", json=new_emp)
    assert response.status_code == 201
    assert response.json()['name'] == "Yash"

def test_get_by_id():
    response = client.get("/employees/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Yash"

def test_get_employee_not_found():
    response = client.get("/employees/69")
    assert response.status_code == 404
    assert response.json()["detail"] == "employee not found:("

def test_delete_employee():
    response = client.delete("/employees/2")
    assert response.status_code == 422

def test_update_employee():
    new_emp = {
        "id": 2,
        "name": "Yash",
        "department": "ML",
        "salary": 100000,
    }
    response = client.put("/employees/2", json=new_emp)
    assert response.status_code == 200
    assert response.json()["salary"] == 100000