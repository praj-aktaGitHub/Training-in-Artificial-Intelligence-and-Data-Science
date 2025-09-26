CREATE database Schooldb;
USE Schooldb;

CREATE TABLE Students(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
age INT,
course VARCHAR(50),
marks INT
);

INSERT INTO Students( name, age, course, marks)
VALUES('Aaryan', 18, 'DS', 78), ('Rudra', 21, 'ML', 60), ('Yash', 24, 'AI', 80);

SELECT * FROM Students

SELECT * FROM Students WHERE marks > 70

SELECT name, age FROM Students


UPDATE Students
SET age = 19, marks = 90
WHERE name = 'Aaryan'

SELECT * FROM Students WHERE name = 'Aaryan'
