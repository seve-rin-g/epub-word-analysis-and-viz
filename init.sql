create schema ol_bookdb;

create table ol_bookdb.book (
    id serial primary key,
    title text,
    author text
);

create table ol_bookdb.word_frequency (
    id serial primary key,
    book_id integer references ol_bookdb.book(id),
    word text,
    frequency integer 
);