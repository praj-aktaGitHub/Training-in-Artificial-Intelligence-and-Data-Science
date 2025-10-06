# from readwritejson import Student

class Student:
    def __init__(self, name, age, email, gender):
        self.name = name,
        self.age = age,
        self.email = email,
        self.gender = gender

data = {"name": "Aaryan", "age": 19 , "email": "aryan123@gmail.com", "gender": "male"}

student = Student(**data)
print(student)
print(student.age)
