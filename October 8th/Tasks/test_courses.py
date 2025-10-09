from http.client import responses

from fastapi.testclient import TestClient
from courses import app, Course

client = TestClient(app)

def test_course():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_course():
    new_course = {
        "id": 2,
        "title": "Python Advanced Course",
        "duration": 60,
        "fee": 4500,
        "is_active": True,
    }

    response = client.post("/courses/", json=new_course)
    assert response.status_code == 201
    assert response.json()["title"] == "Python Advanced Course"

def test_validate_course():
    new_course = {
        "id": 2,
        "title": "AI",
        "duration": 0,
        "fee": -500,
        "is_active": True
    }
    response = client.post("/courses/", json=new_course)
    assert response.status_code == 422
    assert response.json()["detail"] == "Errors for duration and fee"

def test_duplicate_course():
    new_course = {
        "id": 2,
        "title": "Python Advanced Course",
        "duration": 60,
        "fee": 4500,
        "is_active": True,
    }
    response = client.post("/courses/", json=new_course)
    assert response.status_code == 400
    assert response.json()['detail'] == "Course ID already exists"

def test_check_fields_and_types():
    response = client.get("/courses")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all("id" in course for course in data)
    assert all("title" in course for course in data)
    assert all("duration" in course for course in data)
    assert all("fee" in course for course in data)
    assert all("is_active" in course for course in data)


