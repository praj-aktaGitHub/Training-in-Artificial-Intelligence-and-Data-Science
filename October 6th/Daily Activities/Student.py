from pydantic import BaseModel

class Student(BaseModel):
    name : str
    age : int
    email : str
    gender : str

data = {"name": "Aaryan", "age": 20, "email": "aryan123@gmail.com", "gender": "M"}
student = Student(**data)
print(student.name)
print(student.age)
