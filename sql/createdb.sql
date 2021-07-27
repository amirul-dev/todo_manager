drop table if exists todo;

drop table if exists users;

create table todo (
       id integer primary key AUTOINCREMENT not null,
       title text not null,
       description text,
       due_date date,
       due_time timestamp,
       status text);

create table shopping (
       id integer primary key AUTOINCREMENT not null,
       item text not null,
       status text);

create table users (
       id integer primary key AUTOINCREMENT not null,
       name text not null,
       email text not null,
       password text not null);

insert into users (name, email, password) values ('amirul', 'amirul@mail.com', '12345');
