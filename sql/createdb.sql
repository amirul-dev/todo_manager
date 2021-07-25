drop table if exists todo;

create table todo (
       id serial primary key,
       title text,
       description text);
