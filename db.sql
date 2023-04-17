-- create schema estartup;

create table clients(
	clientid int not null primary key auto_increment unique,
    employeeid int,
	password varchar(40) unique,
    name varchar(40),
    surname varchar(40),
    email varchar(40),
    phone varchar(40),
    accountname varchar(40)
);

create table projects(
	projectid int not null primary key auto_increment unique ,
    clientid int,
	name varchar(40),
	cost float
);

create table technologies(
	techid int not null primary key auto_increment unique,
    projectid int,
    name varchar(40)
);

create table employee(
	employeeid int not null primary key auto_increment unique,
	name varchar(40),
    surname varchar(40),
    budget int
);

create table organisation(
	adminpassword varchar(40),
    adminname varchar(40),
	name varchar(40),
    type varchar(40),
    financialdata float
);

alter table projects add constraint fk1 foreign key(clientid) references clients(clientid) on delete cascade on update cascade; 
alter table technologies add constraint fk2 foreign key(projectid) references projects(projectid) on delete cascade on update cascade;
alter table clients add constraint fk3 foreign key(employeeid) references employee(employeeid) on delete cascade on update cascade;

insert into employee(name,surname,budget) values('Darius','Manolescu',2000);
insert into employee(name,surname,budget) values('Andrei','Chirica',1000);

insert into clients (employeeid,password ,name,surname,email,phone,accountname) values('1','client','Darius','Manolescu','manoles@yahoo.com','1234','clien1');
insert into clients (employeeid,password ,name,surname,email,phone,accountname) values('1','client2','Andrei','Chirica','chirica@yahoo.com','12345','client2');

insert into organisation(adminpassword, adminname, name, type, financialdata) values ('admin','admin','eStartUp','SRL','1000'); 

table clients;
table organisation;
table projects;
table technologies;
table employee;


select DISTINCT 
	p.name,
    p.cost,
    t.name
from clients c inner join 
projects p on(c.clientid = p.clientid)
inner join 
technologies t on(t.projectid = p.projectid)
where c.clientid = 2;

select DISTINCT 
	p.name,
    p.cost,
    t.name
from clients c inner join 
projects p on(c.clientid = p.clientid)
inner join 
technologies t on(t.projectid = p.projectid)
where c.clientid = 2;

select * from clients;

select 
	e.surname,
    c.accountname,
	p.name,
    p.cost,
    t.name
from employee e 
inner join
clients c on(e.employeeid = c.employeeid) 
inner join 
projects p on(c.clientid = p.clientid)
inner join 
technologies t on(t.projectid = p.projectid);
	
