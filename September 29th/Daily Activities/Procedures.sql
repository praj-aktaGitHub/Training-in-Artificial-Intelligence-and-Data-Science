create database retaildb;
use retaildb;

create table customers(
custid int auto_increment primary key,
name varchar(50),
city varchar(50),
phone varchar(10)
);

create table products (
prodid int auto_increment primary key,
prodname varchar(50),
category varchar(50),
price decimal(10, 2)
);

create table orders (
orderid int auto_increment primary key,
custid int,
order_date date,
foreign key (custid) references customers(custid)
);

create table orderdetails (
orderdetailid int auto_increment primary key,
orderid int,
prodid int,
quantity int,
foreign key (orderid) references orders (orderid),
foreign key (prodid) references products(prodid)
);

INSERT INTO customers (name, city, phone) VALUES
('Rahul', 'Mumbai', '9876543210'),
('Priya', 'Delhi', '9876501234'),
('Arjun', 'Bengaluru', '9876512345'),
('Neha', 'Hyderabad', '9876523456');

INSERT INTO products (prodname, category, price) VALUES
('Laptop', 'Electronics', 60000.00),
('Smartphone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Shoes', 'Fashion', 3500.00),
('T-Shirt', 'Fashion', 1200.00);

INSERT INTO orders (custid, order_date) VALUES
(1, '2025-09-01'),
(2, '2025-09-02'),
(3, '2025-09-03'),
(1, '2025-09-04');

INSERT INTO orderdetails (orderid, prodid, quantity) VALUES
(1, 1, 1),   -- Rahul bought 1 Laptop
(1, 3, 2),   -- Rahul bought 2 Headphones
(2, 2, 1),   -- Priya bought 1 Smartphone
(3, 4, 1),   -- Arjun bought 1 Shoes
(4, 5, 3);   -- Rahul bought 3 T-Shirts

delimiter //
-- create procedure getallprod()
-- begin
-- select prodid, prodname, category, price
-- from products;
-- end //
-- delimiter ;

-- call getallprod();

delimiter //
create procedure getorderofcust()
begin
select o.orderid, o.order_date, c.name as custname
from orders o
join customers c
on o.custid = c.custid;
end //
delimiter ;

call getorderofcust

delimiter //
create procedure getprodinfo()
begin
select o.orderid,
c.name as custname,
p.prodname, od.quantity, p.price, (od.quantity * p.price) as total
from orders o
join customers c on o.custid = c.custid
join orderdetails od on o.orderid = od.orderid
join products p on od.prodid = p.prodid;

end //
delimiter ;

call getprodinfo


delimiter //
create procedure getprodinfoofcust(IN customerid int)
begin
select o.orderid,
o.order_date,
p.prodname,
od.quantity,
p.price,
(od.quantity * p.price) as total
from orders o
join orderdetails od on o.orderid = od.orderid
join products p on od.prodid = p.prodid
where o.custid = customerid;
end //
delimiter ;
call getprodinfoofcust(1);


delimiter //
create procedure getmonthlysales(in monthno int, in yearno int)
begin
select month(o.order_date) as month, year(o.order_date) as year,
sum(od.quantity * p.price) as totalsales
from orders o
join orderdetails od on o.orderid = od.orderid
join products p on od.prodid = p.prodid
where month(o.order_date) = monthno and year(o.order_date) = yearno
group by month, year;
end //
delimiter ;
call getmonthlysales(9, 2025);

DELIMITER $$
CREATE PROCEDURE GetTopthreeProducts()
BEGIN
SELECT p.prodname,
SUM(od.quantity) AS total_sold,
SUM(od.quantity * p.price) AS revenue
FROM  orderdetails od
join products p on od.prodid = p.prodid
GROUP BY p.prodid, p.prodname
order by revenue DESC
LIMIT 3;
END $$
DELIMITER ;
 
CALL GetTopthreeProducts();


