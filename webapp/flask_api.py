"""
This module provides functionality of RESTful APIs.
Two sets of APIs are provided:
    1. Book Get, Create, Update, Delete API
    2. User Get, Create, Update, Delete API (for future use)
Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
"""

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()


# Declaring the model.
class Person(db.Model):
    """
    Person class define Person data model corresponding to LmsUser table.

    Attributes:
        LmsUserID: Unique identifier
        Username: Username used for user to log in
        Name: User's full name

    """
    __tablename__ = "LmsUser"
    LmsUserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(256), unique=True)
    Name = db.Column(db.Text)

    def __init__(self, Name, Username, LmsUserID=None):
        self.LmsUserID = LmsUserID
        self.Username = Username
        self.Name = Name


class PersonSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("LmsUserID", "Username", "Name")


class Book(db.Model):
    """
    Book class define Book data model corresponding to Book table.

    Attributes:
        BookID: Unique identifier
        ISBN: Book's ISBN number
        Title: Book's title
        Author: Book's Author
        Status: Book's Borrow Status
        PublishedDate: Book's publication date in the Date format

    """
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ISBN = db.Column(db.String(20), nullable=False, unique=True)
    Title = db.Column(db.Text, nullable=False)
    Author = db.Column(db.Text, nullable=False)
    PublishedDate = db.Column(db.Date, nullable=False)

    # Class constructor - make BookID None so it can be auto-incremental
    def __init__(self, ISBN, Title, Author, PublishedDate, BookID=None):
        self.BookID = BookID
        self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate


class BookSchema(ma.Schema):
    """
    BookSchema class define Book ORM schema corresponding to Book table.

    """
    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("BookID", "ISBN", "Title", "Author", "PublishedDate")


PERSON_SCHEMA = PersonSchema()
PEOPLE_SCHEMA = PersonSchema(many=True)

BOOK_SCHEMA = BookSchema()
BOOKS_SCHEMA = BookSchema(many=True)


# API endpoints for book CRUD operations
@api.route("/book", methods=["GET"])
def get_books():
    """API that retrieves all the books' information in the DB

    Returns:
        All book info in Json format.

    """
    books = Book.query.all()
    result = BOOKS_SCHEMA.dump(books)

    return jsonify(result.data)


# Endpoint to get book by id.
@api.route("/book/<book_id>", methods=["GET"])
def get_book(book_id):
    """API that retrieves one book with specific book id

    Returns:
        Specific book's information in Json format.
        Example :
        {
            "Author": "Suzanne Collins",
            "BookID": 1,
            "ISBN": "978-0439023528",
            "PublishedDate": "2010-01-02",
            "Title": "The Hunger Games"
        }

    """
    book = Book.query.get(book_id)

    return BOOK_SCHEMA.jsonify(book)


# Endpoint to create new book.
@api.route("/book", methods=["POST"])
def add_book():
    """API that adds a book to cloud DB

    Returns:
        When successful, return the detailed information of the newly created
        book

    """
    isbn = request.json["isbn"]
    title = request.json["title"]
    author = request.json["author"]
    pub_date = request.json["pubDate"]

    new_book = Book(ISBN=isbn,
                    Title=title,
                    Author=author,
                    PublishedDate=pub_date)

    db.session.add(new_book)
    db.session.commit()

    return BOOK_SCHEMA.jsonify(new_book)


# Endpoint to update book.
@api.route("/book/<book_id>", methods=["PUT"])
def update_book(book_id):
    """API that update the detailed information of a book with specific bookid

    Returns:
        When successful, return the detailed information after updating

    """
    book = Book.query.get(book_id)
    print(book)

    book.Title = request.json['title']
    book.ISBN = request.json['isbn']
    book.Author = request.json['author']
    book.PublishedDate = request.json['pubDate']

    db.session.commit()

    return BOOK_SCHEMA.jsonify(book)


# Endpoint to delete a book.
@api.route("/book/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    """API that deletes a book with specific bookid

    Returns:
        When successful, return the information of the deleted book

    """
    book = Book.query.get(book_id)
    # Add condition required - if book not available
    db.session.delete(book)
    db.session.commit()

    return BOOK_SCHEMA.jsonify(book)


# API endpoints for user CRUD operation ###
# Endpoint to show all LmsUsers.
@api.route("/person", methods=["GET"])
def get_people():
    people = Person.query.all()
    result = PEOPLE_SCHEMA.dump(people)

    return jsonify(result.data)


# Endpoint to get person by id.
@api.route("/person/<person_id>", methods=["GET"])
def get_person(person_id):
    person = Person.query.get(person_id)

    return PERSON_SCHEMA.jsonify(person)


# Endpoint to create new person.
@api.route("/person", methods=["POST"])
def add_person():
    name = request.json["name"]
    username = request.json["username"]

    new_person = Person(Name=name, Username=username)

    db.session.add(new_person)
    db.session.commit()

    return PERSON_SCHEMA.jsonify(new_person)


# Endpoint to update person.
@api.route("/person/<person_id>", methods=["PUT"])
def update_person(person_id):
    person = Person.query.get(person_id)
    name = request.json["name"]

    person.Name = name
    db.session.commit()

    return PERSON_SCHEMA.jsonify(person)


# Endpoint to delete person.
@api.route("/person/<person_id>", methods=["DELETE"])
def delete_person(person_id):
    person = Person.query.get(person_id)

    db.session.delete(person)
    db.session.commit()

    return PERSON_SCHEMA.jsonify(person)
