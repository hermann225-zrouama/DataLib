# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for,jsonify

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
#from app.mod_book.forms import LoginForm

# Import module models (i.e. User)
from app.mod_book.models import Book

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_book = Blueprint('book', __name__, url_prefix='/book')

# Get the last book on home page
@mod_book.route('/last', methods=['GET'])
def fetch_last_book():
        #get the all book
        books = Book.query.order_by(Book.id.desc()).limit(6).all()
        
        if books:
            return books 
        else:
            return 'NBF'
