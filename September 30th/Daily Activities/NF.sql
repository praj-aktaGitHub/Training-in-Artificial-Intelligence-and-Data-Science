create database RetailNF;
use RetailNF;

create table badorders (
orderid int primary key,
order_date DATE,
custid int,
custname varchar(50),
custcity varchar(50),
prodid varchar(200),
prodname varchar(200),
unitprices varchar(200),
quantities varchar(200),
order_total decimal(10, 2)
);

INSERT INTO badorders VALUES
-- order_id, date, cust, name, city,     pids,      pnames,                   prices,        qtys,    total
(101, '2025-09-01', 1, 'Rahul', 'Mumbai', '1,3',    'Laptop,Headphones',      '60000,2000',  '1,2',   64000.00),
(102, '2025-09-02', 2, 'Priya', 'Delhi',  '2',      'Smartphone',             '30000',       '1',     30000.00);

1NF 


create table order_1nf (
orderid int primary key,
order_date DATE,
custid int,
custname varchar(50),
custcity varchar(50)
);

create table orderitems_nf1(
orderid int ,
lineno int,
prodid int,
prodname varchar(50),
unitprices decimal(10,2),
quantity int,
primary key (orderid, lineno),
foreign key (orderid) references order_1nf(orderid)
);

insert into order_1nf
select orderid, order_date, custid, custname, custcity
from badorders;

insert into orderitems_nf1 values
(101, 1, 1, 'Laptop', 60000, 1), 
(101, 2, 3, 'Headphones', 2000, 2);

insert into orderitems_nf1 values
(102, 1, 2, 'Smartphone', 30000, 1);

select * from orderitems_nf1;

2NF


create table cust_2nf(
custid int primary key,
custname varchar(50),
custcity varchar(50)
);

create table order_2nf(
orderid int primary key,
order_date date,
custid int,
foreign key (custid) references cust_2nf(custid)
);

create table prod_2nf(
prodid int primary key,
prodname varchar(50),
category varchar(50),
lastprice decimal(10,2)
);

CREATE TABLE orderitems_2NF (
  orderid INT,
  lineno INT,
  prodid INT,
  unit_price_at_sale DECIMAL(10,2),  -- historical price
  quantity INT,
  PRIMARY KEY (orderid, lineno),
  FOREIGN KEY (orderid) REFERENCES order_2NF(orderid),
  FOREIGN KEY (prodid) REFERENCES prod_2NF(prodid)
);

INSERT INTO cust_2NF VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi');
 
INSERT INTO prod_2NF VALUES
(1, 'Laptop',     'Electronics', 60000),
(2, 'Smartphone', 'Electronics', 30000),
(3, 'Headphones', 'Accessories',  2000);
 
INSERT INTO order_2NF VALUES
(101, '2025-09-01', 1),
(102, '2025-09-02', 2);
 
INSERT INTO orderitems_2NF VALUES
(101, 1, 1, 60000, 1),
(101, 2, 3,  2000, 2),
(102, 1, 2, 30000, 1);

3NF

create table cities(
cityid int primary key,
cityname varchar(50),
state varchar(50)
);

create table cust_3nf(
custid int primary key,
custname varchar(50),
cityid int,
foreign key (cityid) references cities(cityid)
);

create table prod_3nf like prod_2nf;
insert into prod_3nf select * from prod_2nf;

create table order_3nf like order_2nf;
insert into order_3nf select * from order_2nf;

insert into cities values 
(10, 'Mumbai', 'Maharashtra'),
(20, 'Delhi', 'Delhi');

insert into cust_3nf values
(1, 'Aaryan', 10),
(2, 'Rudra', 20);

create table orderitems_3nf like orderitems_2nf;
insert into orderitems_3nf select * from orderitems_2nf;


