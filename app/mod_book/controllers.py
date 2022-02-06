# Import flask dependencies
import datetime
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
from app.mod_auth.models import User


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_book = Blueprint('book', __name__, url_prefix='/book')

# Get the last book on home page
@mod_book.route('/last', methods=['GET'])
def fetch_last_book():
        """ return last six books from database"""
        books = Book.query.order_by(Book.isbn.desc()).limit(6).all()
        
        if books:
            return books 
        else:
            return 'NBF'


@mod_book.route('', methods=['GET'])
@mod_book.route('/', methods=['GET'])
def fetch_all_book():
    """Return all book from database in desc order"""
    books = Book.query.order_by(Book.isbn.desc()).all()
    if books:
        session['books'] = books
        return books 
    else:
        return 'NBF'


@mod_book.route('/register', methods=['GET','POST'])
def register_book():
    """Register a new book"""
    form = request.form
    if request.method == 'POST':
        book = Book(form['titre'].strip(),form['auteur'],form['edition'],form['isbn'].strip(),form['nbexemplar'],form['category'],form['year'])

        try:
            db.session.add(book)
            db.session.commit()

            flash('Thanks for registering')

            return redirect(url_for('data_lib.dash_livres'))
        except:
            return redirect(url_for('data_lib.dash_livres'))

    else:
        return redirect(url_for('data_lib.dash_livres'))



@mod_book.route('/update/<isbn>', methods=['GET'])
def update_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        user = session['user']
        session['book_update_isbn'] = isbn
        return render_template("auth/profile/dashboard/update_book.html", book = book,user=user)
    else:
        return redirect(url_for("data_lib.dash_livres"))

@mod_book.route('/update', methods=['POST'])
def update():
    form = request.form
    if request.method == 'POST':
        book = Book.query.filter_by(isbn=session['book_update_isbn']).first()

        book.title = form['titre'].strip()
        book.isbn = form['isbn'].strip()
        book.author = form['auteurs']
        book.edition = form['edition']
        book.nbExemplar = form['nbExemplar']
        book.category = form['category']
        book.year = form['date']

        db.session.commit()
        return redirect(url_for('data_lib.dash_livres'))
        
@mod_book.route('/delete/<isbn>', methods=['GET','POST'])  
def delete_book(isbn):
    """
    Goal : Delete a book

    Method : GET 

    Args: (isbn) of the book to delete
    """

    book = Book.query.filter_by(isbn=isbn).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('data_lib.dash_livres'))

@mod_book.route('/<isbn>',methods =['GET'])
def get_book_by_isbn(isbn):
    #get book by isbn
    book = Book.query.filter_by(isbn=isbn).first()
    if 'user' in session:
        user = session['user']
        code = f"LIB{datetime.datetime.now().strftime('%d%M%S')}"
        return render_template("auth/book.html",book_info = book,user = user,code = code)
    else:
       return redirect(url_for('auth.signin'))
    

######FONCTION PERSO###############
def general_info():
    """
    return general info about the library

    output : nb_boook,nb_user
    """
    nb_book = Book.query.count()
    nb_user = User.query.count()
    return {'nb_book':nb_book,'nb_user':nb_user}

def getBookInfo(isbn):
    return Book.query.filter_by(isbn=isbn.strip()).first()

def getAllBook():
    return Book.query.all()