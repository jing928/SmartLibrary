-- replace with real database name
Use SmartLibrary; 

-- Create Database Schema
create table LmsUser
(
    LmsUserID int           not null auto_increment,
    UserName  nvarchar(256) not null,
    Name      text          not null,
    constraint PK_LmsUser primary key (LmsUserID),
    constraint UN_UserName unique (UserName)
);

create table Book
(
    BookID        int                              not null auto_increment,
    ISBN          nvarchar(20)                     not null,
    Title         text                             not null,
    Author        text                             not null,
    PublishedDate date                             not null,
    Status        enum ('available','unavailable') not null default 'available',
    constraint PK_Book primary key (BookID),
    constraint UN_ISBN unique (ISBN)
);

create table BookBorrowed
(
    BookBorrowedID  int  not null auto_increment,
    LmsUserID       int  not null,
    BookID          int  not null,
    Status          enum ('borrowed', 'returned'),
    BorrowedDate    date not null,
    ReturnedDate    date null,
    CalendarEventID text,
    constraint PK_BookBorrowed primary key (BookBorrowedID),
    constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references LmsUser (LmsUserID),
    constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
);

-- Insert data to User table
insert into LmsUser (UserName, Name) values ('jing', 'Jing Li');
insert into LmsUser (UserName, Name) values ('cheng', 'Charles Cheng');
insert into LmsUser (UserName, Name) values ('flydog', 'Yanan Guo');
insert into LmsUser (UserName, Name) values ('qian', 'Darren Qian');

-- Insert data to Book table
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-0439023528', 'The Hunger Games', 'Suzanne Collins', '2010-01-01');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-0545139700', 'Harry Potter and the Deathly Hallows', 'J. K. Rowling', '2009-07-01');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-0345803481', 'Fifty Shades of Grey', 'E L James', '2012-04-03');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-1449355739', 'Learning Python', 'Mark Lutz', '2013-07-06');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-1118311806', 'Beginning ASP.NET 4.5', 'Imar Spaanjaars', '2012-11-06');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-1348334526', 'Becoming', 'Michelle Obama', '2018-07-06');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-1678872329', 'The Wonky Donkey', 'Craig Smith', '2018-10-06');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-0307588371', 'Gone Girl', 'Gillian Flynn', '2014-04-22');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-0857523921', 'The Girl on the Train', 'Paula Hawkins', '2015-01-13');
insert into Book (ISBN, Title, Author, PublishedDate)
values ('978-1982129736', 'The Mueller Report', 'The Washington Post', '2019-03-01');
