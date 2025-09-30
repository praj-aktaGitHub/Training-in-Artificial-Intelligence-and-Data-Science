create database Capstone;
use Capstone;

create table Patients (
patient_id INT PRIMARY KEY,
name VARCHAR(50),
age INT,
gender CHAR(1),
city VARCHAR(50)
);

create table Doctors(
doctor_id INT PRIMARY KEY,
name VARCHAR(50),
specialization VARCHAR(50),
experience int
);

create table Appointments(
appointment_id INT PRIMARY KEY,
patient_id INT,
doctor_id INT,
appointment_date DATE,
status VARCHAR(20)
);

create table MedicalRecords(
record_id INT PRIMARY KEY,
patient_id INT,
doctor_id INT,
diagnosis VARCHAR(100),
treatment VARCHAR(100),
date DATE
);

create table Billing(
bill_id INT PRIMARY KEY,
patient_id INT,
amount DECIMAL(10,2),
bill_date DATE,
status VARCHAR(20)
);


INSERT INTO Patients (patient_id, name, age, gender, city) VALUES
(1, 'Aarohi Deshmukh', 28, 'F', 'Pune'),
(2, 'Harpreet Singh', 35, 'M', 'Amritsar'),
(3, 'Meera Jadhav', 42, 'F', 'Mumbai'),
(4, 'Gurpreet Kaur', 30, 'F', 'Ludhiana'),
(5, 'Rohan Pawar', 25, 'M', 'Nashik'),
(6, 'Tanvi Shinde', 33, 'F', 'Kolhapur'),
(7, 'Rajveer Gill', 40, 'M', 'Jalandhar'),
(8, 'Snehal More', 29, 'F', 'Aurangabad'),
(9, 'Baljeet Singh', 50, 'M', 'Patiala'),
(10, 'Sayali Kulkarni', 22, 'F', 'Nagpur');


INSERT INTO Doctors (doctor_id, name, specialization, experience) VALUES
(101, 'Dr. Vishal Patil', 'Cardiology', 12),
(102, 'Dr. Simranjeet Kaur', 'Dermatology', 8),
(103, 'Dr. Sandeep Bhosale', 'Orthopedics', 15),
(104, 'Dr. Manpreet Singh', 'Pediatrics', 10),
(105, 'Dr. Snehal Kulkarni', 'General Medicine', 6);


INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES
(1001, 1, 101, '2025-09-20', 'Completed'),
(1002, 2, 102, '2025-09-21', 'Scheduled'),
(1003, 3, 103, '2025-09-22', 'Cancelled'),
(1004, 4, 104, '2025-09-23', 'Completed'),
(1005, 5, 105, '2025-09-24', 'Scheduled'),
(1006, 6, 101, '2025-09-25', 'Completed'),
(1007, 7, 102, '2025-09-26', 'Scheduled'),
(1008, 8, 103, '2025-09-27', 'Completed'),
(1009, 9, 104, '2025-09-28', 'Cancelled'),
(1010, 10, 105, '2025-09-29', 'Scheduled');

INSERT INTO MedicalRecords (record_id, patient_id, doctor_id, diagnosis, treatment, date) VALUES
(2001, 1, 101, 'Hypertension', 'Medication and lifestyle changes', '2025-09-20'),
(2002, 2, 102, 'Skin Allergy', 'Antihistamines and creams', '2025-09-21'),
(2003, 3, 103, 'Back Pain', 'Physiotherapy and rest', '2025-09-22'),
(2004, 4, 104, 'Cold and Cough', 'Syrup and steam inhalation', '2025-09-23'),
(2005, 5, 105, 'Fever', 'Paracetamol and hydration', '2025-09-24'),
(2006, 6, 101, 'Chest Pain', 'ECG and medication', '2025-09-25'),
(2007, 7, 102, 'Acne', 'Topical treatment', '2025-09-26'),
(2008, 8, 103, 'Fracture', 'Casting and painkillers', '2025-09-27'),
(2009, 9, 104, 'Flu', 'Rest and antiviral drugs', '2025-09-28'),
(2010, 10, 105, 'Headache', 'Painkillers and hydration', '2025-09-29');

INSERT INTO Billing (bill_id, patient_id, amount, bill_date, status) VALUES
(3001, 1, 1500.00, '2025-09-20', 'Paid'),
(3002, 2, 800.00, '2025-09-21', 'Unpaid'),
(3003, 3, 1200.00, '2025-09-22', 'Paid'),
(3004, 4, 600.00, '2025-09-23', 'Paid'),
(3005, 5, 1000.00, '2025-09-24', 'Unpaid'),
(3006, 6, 1800.00, '2025-09-25', 'Paid'),
(3007, 7, 900.00, '2025-09-26', 'Unpaid'),
(3008, 8, 2000.00, '2025-09-27', 'Paid'),
(3009, 9, 700.00, '2025-09-28', 'Paid'),
(3010, 10, 1100.00, '2025-09-29', 'Unpaid');


select p.name 
from Patients p
join Appointments a on p.patient_id = a.patient_id
join Doctors d on a.doctor_id = d.doctor_id
where specialization = 'Cardiology';

select d.name, count(a.appointment_id) 
from Doctors d
join Appointments a on d.doctor_id = a.doctor_id
group by d.name, d.doctor_id;

select b.patient_id, p.name, b.bill_id, b.amount, b.bill_date
from Patients p
join Billing b on p.patient_id = b.patient_id
where status = 'Unpaid';

-- Stored Procedures
drop procedure getpatienthist;
delimiter //
create procedure getpatienthist(in patientid int)
begin
select m.record_id, a.appointment_id,
 p.name as Patient_name, d.name as Doc_name, a.appointment_date, m.diagnosis, m.treatment
from MedicalRecords m 
join Patients p on m.patient_id = p.patient_id
join Doctors d on m.doctor_id = d.doctor_id 
join Appointments a on d.doctor_id = a.doctor_id
where m.patient_id = patientid;
end//
delimiter ;
call getpatienthist(5);

delimiter //
create procedure GetDocAppointments(in docid int)
begin
select a.appointment_id, a.appointment_date, a.doctor_id, d.name as Doc_Name, a.status
from Appointments a 
join Doctors d on a.doctor_id = d.doctor_id
where d.doctor_id = docid;
end //
delimiter ;
call GetDocAppointments(101);



