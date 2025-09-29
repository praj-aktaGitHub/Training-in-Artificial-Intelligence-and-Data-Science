create database school;
use school;
 
create table teachers(
teachid int auto_increment primary key, name varchar(50), subid int
);

create table subjects (
subid int auto_increment primary key, subname varchar(50)
);

INSERT INTO teachers (name, subid) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English

select * from teachers

INSERT INTO subjects (subname) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

select * from subjects

select t.name
from teachers t
inner join subjects s on t.subid = s.subid;

select t.name
from teachers t
left join subjects s on t.subid = s.subid;

select t.name
from teachers t
right join subjects s on t.subid = s.subid;

select t.name, s.subname
from teachers t
left join subjects s on t.subid = s.subid;
union 
select t.name, s.subname
from teachers t
right join subjects s on t.subid = s.subid;


