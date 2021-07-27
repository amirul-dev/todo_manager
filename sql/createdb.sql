drop table if exists todos;

drop table if exists users;

drop table if exists shopping;

create table todos (
       id integer primary key AUTOINCREMENT not null,
       userid integer not null,
       title text not null,
       description text,
       due_date date,
       due_time timestamp,
       status text
       FOREIGN KEY (userid) references users(id) ON DELETE CASCADE);

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
