# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from dataclasses import dataclass

# Define a base model for other database tables to inherit


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.String(128),  default=db.func.current_timestamp())
    date_modified = db.Column(db.String(128),  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())

# Define a Book model
@dataclass
class Book(Base):

    __tablename__ = 'book'

    # Book title
    title = db.Column(db.String(128),  nullable=False)

    # Identification Data: isbn, author, year, nbExemplar,category,available
    isbn = db.Column(db.String(128),  nullable=False, unique=True)
    author = db.Column(db.String(128),  nullable=False)
    edition = db.Column(db.String(192),  nullable=False)
    nbExemplar = db.Column(db.Integer,  nullable=False, default=1)
    category = db.Column(db.String(128),  nullable=False)
    available = db.Column(db.SmallInteger, nullable=False, default=1)
    year = db.Column(db.Integer,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, title, author, edition,isbn,nbExemplar,category,year):
        self.title = title
        self.author = author
        self.edition = edition
        self.isbn = isbn
        self.nbExemplar = nbExemplar
        self.category = category
        self.year = year

    def __repr__(self):
        return '<Book %r>' % (self.title)
