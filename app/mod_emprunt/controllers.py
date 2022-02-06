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
from app.mod_emprunt.models import Emprunt
from app.mod_book.controllers import getBookInfo


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_book = Blueprint('book', __name__, url_prefix='/book')

# Get the last book on home page
def nb_to_mois(ch):
    mois = {
        "0":"Janvier",
        "1":"Février",
        "2":"Mars",
        "3":"Avril",
        "4":"Mai",
        "5":"Juin",
        "6":"Juillet",
        "7":"Aout",
        "8":"Septembre",
        "9":"Octobre",
        "10":"Novembre",
        "11":"Decembre"
    }
    return mois[ch]

def fetch_emprunt(matricule):
    emprunts = Emprunt.query.filter_by(user=matricule,statut=1).all()
    e = []
    
    for emprunt in emprunts:
        e.append({"info":emprunt,"date":nb_to_mois(str(datetime.datetime.strptime(emprunt.date_emprunt,'%Y-%m-%d').month)) ,"book":getBookInfo(emprunt.book).title})
    taille = len(e)
    return {"e":e,"taille":taille}

        