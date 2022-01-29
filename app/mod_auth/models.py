# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'user'

    # User Name
    nom = db.Column(db.String(128),  nullable=False)
    # Identification Data: email & password & matricule
    matricule = db.Column(db.String(128),  nullable=False, unique=True,primary_key=True)
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role = db.Column(db.SmallInteger, nullable=False, default=0)
    status = db.Column(db.SmallInteger, nullable=False, default=1)

    # New instance instantiation procedure
    def __init__(self, nom, email, password,matricule):

        self.nom = nom
        self.email = email
        self.password = password
        self.matricule = matricule

    def __repr__(self):
        return '<User %r>' % (self.nom)
