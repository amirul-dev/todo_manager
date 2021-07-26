drop table if exists todo;

drop table if exists users;

create table todo (
       id integer primary key AUTOINCREMENT not null,
       title text not null,
       description text,
       due_time timestamp);

create table users (
       id integer primary key AUTOINCREMENT not null,
       name text not null,
       email text not null,
       password text not null);

insert into users (name, email, password) values ('amirul', 'amirul@mail.com', '12345');
