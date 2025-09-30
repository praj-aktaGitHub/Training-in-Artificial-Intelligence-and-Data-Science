Create database CompanyDB;
use CompanyDB;

create table depart(
 departid int auto_increment primary key,
 depart_name varchar(50) not null
 );

create table employees(
empid int auto_increment primary key,
name varchar(50),
age int,
salary decimal(10, 2),
departid int,
foreign key(departid) references depart(departid)
);

insert into depart (depart_name) values ('AI'), ('HR'), ('Finance'), ('Sales'), ('Accounts'), ('IT');
insert into employees (name, age, salary, departid) values
('Prajakta', 22, 4800000, 1), ('Aaryan', 26, 400000, 2), ('Shane', 23, 300000, NULL), ('Rudra', 30, 450000, 4), ('Arjun', 28, 900000, 5), ('Krishna', 32, 10000, 5); 
select * from employees

truncate table employees;

alter table employees drop foreign key employees_ibfk_1;

truncate table depart;

select e.name, e.salary, d.depart_name
from employees e 
inner join depart d on e.departid = d.departid;

select * from depart;
select e.name, e.salary
from employees e
left join depart d on e.departid = d.departid;

select e.name, e.salary
from employees e
right join depart d on e.departid = d.departid;

select e.name, e.salary
from employees e
left join depart d on e.departid = d.departid;
union
select e.name, e.salary
from employees e
right join depart d on e.departid = d.departid;
