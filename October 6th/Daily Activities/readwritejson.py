import json

Student = {
  "name": "Aaryan",
  "age" : "19",
  "course":["AI", "ML"],
  "Marks": {"AI": 85, "ML": 90}
}

with open("Student.json", "w")as f:
    json.dump(Student, f, indent=4)

with open("Student.json", "r")as f:
    data = json.load(f)

print(data["name"])
print(data["Marks"]["AI"])