from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
class Person(db.Model):
    __tablename__ = "LmsUser"
    # PersonID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # Name = db.Column(db.Text)
    LmsUserID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Username = db.Column(db.String(256), unique = True)
    Name = db.Column(db.Text)

    def __init__(self, LmsUserID, Name, Username = None):
        self.LmsUserID = LmsUserID
        self.Username = Username
        self.Name = Name

class PersonSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("LmsUserID", "Username", "Name")

class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ISBN = db.Column(db.String(20), nullable = False, unique = True)
    Title = db.Column(db.Text, nullable = False)
    Author = db.Column(db.Text, nullable = False)
    PublishedDate = db.Column(db.Date, nullable = False)

    # Class constructor - make BookID None so it can be auto-incremental
    def __init__(self, ISBN, Title, Author, PublishedDate, BookID = None):
        self.BookID = BookID
        self.ISBN = ISBN
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "ISBN", "Title", "Author", "PublishedDate")

personSchema = PersonSchema()
personsSchema = PersonSchema(many = True)

bookSchema = BookSchema()
booksSchema = BookSchema(many = True)

# API endpoints for book CRUD operations
# Endpoint to show all books.
@api.route("/book", methods = ["GET"])
def getBooks():
    books = Book.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/book/<id>", methods = ["GET"])
def getBook(id):
    book = Book.query.get(id)

    return bookSchema.jsonify(book)

# Endpoint to create new book.
@api.route("/book", methods = ["POST"])
def addBook():
    isbn = request.json["isbn"]
    title = request.json["title"]
    author = request.json["author"]
    pubDate = request.json["pubDate"]

    newBook = Book(ISBN = isbn,
        Title = title, 
        Author = author, 
        PublishedDate = pubDate)

    db.session.add(newBook)
    db.session.commit()

    return bookSchema.jsonify(newBook)

# Endpoint to delete a book.
@api.route("/book/<id>", methods = ["DELETE"])
def bookDelete(id):
    book = Book.query.get(id)
    # Add condition required?
    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)



# API endpoints for user CRUD operation
# Endpoint to show all LmsUsers.
@api.route("/person", methods = ["GET"])
def getPeople():
    people = Person.query.all()
    result = personsSchema.dump(people)

    return jsonify(result.data)

# Endpoint to get person by id.
@api.route("/person/<id>", methods = ["GET"])
def getPerson(id):
    person = Person.query.get(id)

    return personSchema.jsonify(person)

# Endpoint to create new person.
@api.route("/person", methods = ["POST"])
def addPerson():
    name = request.json["name"]

    newPerson = Person(Name = name)

    db.session.add(newPerson)
    db.session.commit()

    return personSchema.jsonify(newPerson)

# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)
