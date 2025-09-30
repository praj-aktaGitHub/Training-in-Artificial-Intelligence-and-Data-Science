CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');

delimiter //
create procedure getallstudents()
begin
select name from Students;
end //
delimiter ;
call getallstudents();

delimiter //
create procedure getallcourses()
begin
select course_name from Courses;
end//
delimiter ;
call getallcourses();

delimiter //
create procedure getstudentfrom_city(in stdcity varchar(50))
begin 
select name 
from Students 
where city  = stdcity;
end //
delimiter ;
call getstudentfrom_city('Mumbai');

delimiter //
create procedure students_withcourses()
begin
select s.name, c.course_name 
from Students s
join Enrollments e on s.student_id = e.student_id
join Courses c on e.course_id = c.course_id;
end//
delimiter ;
call students_withcourses();

delimiter //
create procedure students_enrolled(in courseid int)
begin 
select s.name from Students s
join Enrollments e on s.student_id = e.student_id
join Courses c on e.course_id = c.course_id
where c.course_id = courseid;
end//
delimiter ;
call students_enrolled(101);

delimiter //
create procedure countineach_course()
begin 
select c.course_name, COUNT(e.student_id)
from Enrollments e
join Courses c on e.course_id = c.course_id
group by c.course_id, c.course_name;
end //
delimiter ;
call countineach_course();

delimiter //
create procedure studentswcoursengrade()
begin
select s.name, c.course_name, e.grade
from Students s
join Enrollments e on s.student_id = e.student_id
join Courses c on e.course_id = c.course_id;
end //
delimiter ;
call studentswcoursengrade();

delimiter //
create procedure courses_taken_bystd(in std_id int)
begin
select c.course_name from Courses c
join Enrollments e on c.course_id = e.course_id
where e.student_id = std_id;
end //
delimiter ;
call courses_taken_bystd(1);

delimiter //
create procedure avggrade_course()
begin
select c.course_name, AVG(e.grade)
from Courses c 
join Enrollments e on c.course_id = e.course_id
group by c.course_id, c.course_name;
end//
delimiter ;
call avggrade_course();
