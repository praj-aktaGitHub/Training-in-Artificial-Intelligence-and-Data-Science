CREATE TABLE Employees (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL,
age INT,
department VARCHAR(50),
salary DECIMAL(10, 2)
);

INSERT INTO Employees (name,age,department,salary)
VALUES ('Prajakta', 25, 'Senior Manager', 6000000), ('Saamya', 27, 'Product Manager', 5000000), ('Aaryan', 19, 'HR', 400000), ('Shane', 32, 'Accounting', 580000);

SELECT * FROM Employees
SELECT * FROM Employees WHERE age > 20

UPDATE Employees 
SET department = 'Vice President'
WHERE name = 'Prajakta';

SELECT * FROM Employees 
WHERE name = 'Prajakta'

DELETE FROM Employees WHERE name = 'Saamya'





