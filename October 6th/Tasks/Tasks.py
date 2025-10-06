import logging

logging.basicConfig(
    filename = 'applog2',
    level = logging.INFO,
    format = '%(asctime)s%(levelname)s%(message)s'
)

logging.info('Info Message')

import json

Students = [
{"name": "Rahul", "age": 21, "course": "AI", "marks": 85},
{"name": "Priya", "age": 22, "course": "ML", "marks": 90}
]

with open("Students.json", "w")as f:
    json.dump(Students, f, indent=4)
with open("Students.json", "r")as f:
    data = json.load(f)
logging.info('File saved successfully')


NewStudent = {
    "name": "Arjun", "age": 20, "course": "Data Science", "marks": 78
}

data.append(NewStudent)

with open("Students.json", "w")as f:
    json.dump(data, f, indent = 4)

logging.info('Student added')


print(data)

logging.info('File updated successfully')
logging.debug('debug message')




