create schema ol_bookdb2;

create table ol_bookdb2.book {
    id serial primary key,
    title text,
    author text,
    publication_date date
};

create table ol_bookdb2.word_frequency {
    id serial primary key,
    book_id integer references ol_bookdb.book(id),
    word text,
    frequency integer 
};