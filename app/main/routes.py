# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/
main = Blueprint('data_lib', __name__, url_prefix='/')

from app.mod_book.controllers import fetch_last_book

# Set the route and accepted methods
@main.route('')
@main.route('index')
def index():
    r = fetch_last_book()
    user = None
    #if session user length superior than 0

    if 'user' in session:
        user = session['user']
    return render_template("index.html",books=r,user=user)

@main.route('/<nom>')
def profile(nom):
    if not('user'in session):
       return redirect(url_for('auth.signin'))
    else:
        if (nom == session['user']['nom']):
            return render_template("auth/profile/profile.html",user=session["user"])
        else:
            return '404'

@main.route('/dashboard')
def dash_redirect():
    return redirect(url_for('data_lib.dash_general'))

@main.route('/dashboard/general')
def dash_general():
    if not('user'in session):
       return redirect(url_for('auth.signin'))
    else:
        return render_template("auth/profile/dashboard/general.html",user=session["user"])
        
@main.route('/dashboard/livres')
def dash_livres():
    if not('user'in session):
       return redirect(url_for('auth.signin'))
    else:
        return render_template("auth/profile/dashboard/livres.html",user=session["user"])
    

