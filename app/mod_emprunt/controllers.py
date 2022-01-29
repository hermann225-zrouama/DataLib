# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
import datetime
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm
from app.mod_auth.forms import SignupForm

# Import module models (i.e. User)
from app.mod_emprunt.models import Emprunt
from app.mod_auth.models import User
from app.mod_auth.controllers import getUserById
from app.mod_book.controllers import getBookInfo


#import const
from app.constants.error import ERROR_CREDENTIALS

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_emprunt = Blueprint('emprunt', __name__, url_prefix='/emprunt')

# Set the route and accepted methods


@mod_emprunt.route('/new', methods=['GET', 'POST'])
def new_emprunt():
    emprunts = None
    form = request.form
    user_concerned = getUserById(form['matricule'])
    book_concerned = getBookInfo(form['isbn'])

    emprunts = {
        "date_emprunt": form['dateE'],
        "date_retour": form['dateR'],
        "user": user_concerned,
        "livre": book_concerned,
        "heure": datetime.datetime.now()
    }

    emprunt = Emprunt(form['code'],
                      form['matricule'],
                      form['isbn'],
                      form['dateE'],
                      form['dateR'])

    db.session.add(emprunt)
    db.session.commit()

    return render_template("auth/profile/dashboard/emprunts.html", user=session["user"], empruntEnCours=emprunts)
