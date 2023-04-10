create table clients(
	clientid int not null primary key auto_increment unique,
    employeeid int,
    name varchar(40),
    surname varchar(40),
    email varchar(40),
    phone varchar(40),
    accountname varchar(40),
    password varchar(40)
);

create table projects(
	projectid int not null primary key auto_increment unique ,
    clientid int,
	name varchar(40),
	cost float,
    technologies varchar(40)
);

create table technologies(
	techid int not null primary key auto_increment unique,
    projectid int,
    name varchar(40)
);

create table employee(
	employeeid int not null primary key auto_increment unique,
	name varchar(40),
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

