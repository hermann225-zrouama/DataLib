# Import flask dependencies
from app.mod_book.controllers import getAllBook
from app.mod_auth.controllers import getAllUser
from app.mod_book.controllers import general_info
from app.mod_book.controllers import fetch_all_book
from app.mod_book.controllers import fetch_last_book
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

from app.mod_book.models import Book
import datetime

from app import db

from app.mod_emprunt.models import Emprunt
from app.mod_auth.controllers import getUserById
from app.mod_book.controllers import getBookInfo
from app.mod_emprunt.controllers import fetch_emprunt


# Define the blueprint: 'auth', set its url prefix: app.url/
main = Blueprint('data_lib', __name__, url_prefix='/')


# Set the route and accepted methods

@main.route('')
@main.route('index')
def index():
    r = fetch_last_book()
    user = None
    # if session user length superior than 0

    if 'user' in session:
        user = session['user']
    return render_template("index.html", books=r, user=user)


@main.route('/<nom>')
def profile(nom):
    if not('user' in session):
        return redirect(url_for('auth.signin'))
    else:
        if (nom == session['user']['nom']):
            emprunts_en_cours = fetch_emprunt(session['user']['matricule'])
            return render_template("auth/profile/profile.html", user=session["user"],emprunts=emprunts_en_cours)
        else:
            return '404'


@main.route('/dashboard')
def dash_redirect():
    return redirect(url_for('data_lib.dash_general'))


@main.route('/dashboard/general')
def dash_general():
    info = []
    if not('user' in session):
        return redirect(url_for('auth.signin'))
    else:
        info = general_info()
        info["nb_emprunt"] = Emprunt.query.count()
        #fetch all emprunt
        emprunts = Emprunt.query.all()
        emp = {}
        for emprunt in emprunts:
            emp[emprunt.code] = {'date_retour':emprunt.date_retour,'date_emprunt': emprunt.date_emprunt,'user':getUserById(emprunt.user),'isbn':emprunt.book,'book':getBookInfo(emprunt.book)}
        return render_template("auth/profile/dashboard/general.html", user=session["user"], infos=info,emprunts=emp)


@main.route('/dashboard/livres')
def dash_livres():
    books = None
    if not('user' in session):
        return redirect(url_for('auth.signin'))
    else:
        all_books = fetch_all_book()
        if (all_books):
            books = all_books
            return render_template("auth/profile/dashboard/livres.html", user=session["user"], books=books)
        else:
            return render_template("auth/profile/dashboard/livres.html", user=session["user"], books=books)


@main.route('/dashboard/emprunts', methods=['GET', 'POST'])
def dash_emprunts():
    if request.method == "GET":
        code = f"LIB{datetime.datetime.now().strftime('%d%M%S')}"
        emprunts = None
        if not('user' in session):
            return redirect(url_for('auth.signin'))
        else:
            all_user = getAllUser()
            all_book = getAllBook()
            return render_template("auth/profile/dashboard/emprunts.html", all_book=all_book, all_user=all_user, user=session["user"], empruntEnCours=emprunts,code=code)
    else:
        emprunts = None
        form = request.form
       
        verif1 = Emprunt.query.filter_by(user=form['matricule'], book=form['isbn'],statut = 1).first()
        verif2 = Emprunt.query.filter_by(user=form['matricule'],statut = 1).all()
        print(verif2)
        if (verif1 == None):
            if len(verif2) < 3:
                user_concerned = getUserById(form['matricule'])
                book_concerned = getBookInfo(form['isbn'])

                emprunts = {
                    "date_emprunt": form['dateE'],
                    "date_retour": form['dateR'],
                    "user": user_concerned,
                    "livre": book_concerned,
                    "heure": datetime.datetime.now(),
                    "code": form['code']
                }

                emprunt = Emprunt(code=form['code'],
                                user_mat=form['matricule'],
                                book=form['isbn'],
                                date_emprunt = form['dateE'],
                                date_retour = form['dateR'])
                db.session.add(emprunt)
                db.session.commit()
                return render_template("success.html", user=session["user"], empruntEnCours=emprunts)
            else:
                return render_template("success.html", user=session["user"], empruntEnCours=emprunts,erreur="Nombre d'emprunt max atteint")
        else:
            code = f"LIB{datetime.datetime.now().strftime('%d%M%S')}"
            emprunts = None
            if not('user' in session):
                return redirect(url_for('auth.signin'))
            else:
                all_user = getAllUser()
                all_book = getAllBook()
                if session['user']["role"] ==1:
                    return render_template("success.html", user=session["user"], empruntEnCours=emprunts,erreur="Livre déja emprunté")
                else:
                    return render_template("success.html", user=session["user"], empruntEnCours=emprunts,erreur="Vous avez déja emprunté ce livre et il n'a pas encore été rendu")
