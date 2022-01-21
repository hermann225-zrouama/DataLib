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
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_book = Blueprint('book', __name__, url_prefix='/book')

# Get the last book on home page
@mod_book.route('/last', methods=['GET'])
def fetch_last_book():
        """ return last six books from database"""
        books = Book.query.order_by(Book.id.desc()).limit(6).all()
        
        if books:
            return books 
        else:
            return 'NBF'


@mod_book.route('', methods=['GET'])
@mod_book.route('/', methods=['GET'])
def fetch_all_book():
    """Return all book from database in desc order"""
    books = Book.query.order_by(Book.id.desc()).all()
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
        book = Book(form['titre'],form['auteur'],form['edition'],form['isbn'],form['nbexemplar'],form['category'],form['year'])

        try:
            db.session.add(book)
            db.session.commit()

            flash('Thanks for registering')

            return redirect(url_for('data_lib.dash_livres'))
        except:
            return redirect(url_for('data_lib.dash_livres'))

    else:
        return redirect(url_for('data_lib.dash_livres'))



@mod_book.route('/update/<int:id>', methods=['GET'])
def update_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        user = session['user']
        session['book_update_id'] = id
        return render_template("auth/profile/dashboard/update_book.html", book = book,user=user)
    else:
        return redirect(url_for("data_lib.dash_livres"))

@mod_book.route('/update', methods=['POST'])
def update():
    form = request.form
    if request.method == 'POST':
        book = Book.query.filter_by(id=session['book_update_id']).first()

        book.title = form['titre']
        book.isbn = form['isbn']
        book.author = form['auteurs']
        book.edition = form['edition']
        book.nbExemplar = form['nbExemplar']
        book.category = form['category']
        book.year = form['date']

        db.session.commit()
        return redirect(url_for('data_lib.dash_livres'))
        
@mod_book.route('/delete/<int:id>', methods=['GET','POST'])  
def delete_book(id):
    """
    Goal : Delete a book

    Method : GET 

    Args: (id) of the book to delete
    """

    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('data_lib.dash_livres'))

@mod_book.route('/<int:id>',methods =['GET'])
def get_book_by_id(id):
    #get book by id
    book = Book.query.filter_by(id=id).first()
    if 'user' in session:
        user = session['user']
    else:
        user = []
    return render_template("auth/book.html",book_info = book,user = user)

######FONCTION PERSO###############
def general_info():
    """
    return general info about the library

    output : nb_boook,nb_user
    """
    nb_book = Book.query.count()
    nb_user = User.query.count()
    return {'nb_book':nb_book,'nb_user':nb_user}
