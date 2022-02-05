# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from dataclasses import dataclass

# Define a base model for other database tables to inherit

class Base(db.Model):

    __abstract__ = True

    date_created = db.Column(db.String(128),  default=db.func.current_timestamp())
    date_modified = db.Column(db.String(128),  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())

# Define a Emprunt model
@dataclass
class Emprunt(Base):

    __tablename__ = 'emprunt'

    code = db.Column(db.String(128),  nullable=False, unique=True,primary_key=True)
    user = db.Column(db.String(128),  nullable=False,primary_key=True)
    book = db.Column(db.String(128),  nullable=False,primary_key=True)
    date_emprunt = db.Column(db.String(128),  nullable=False)
    date_retour = db.Column(db.String(128),  nullable=False)
    

    # New instance instantiation procedure
    def __init__(self, **kwargs):
        self.code = kwargs['code']
        self.user = kwargs['user_mat']
        self.date_emprunt = kwargs['date_emprunt']
        self.date_retour = kwargs['date_retour']
        self.book = kwargs['book']

    def __repr__(self):
        return '<Emprunt %r>' % (self.code)