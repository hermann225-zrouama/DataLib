# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm
from app.mod_auth.forms import SignupForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)
    user = []
    # Verify the sign in form
    if request.method == "POST" and form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id
            session['user'] = {
                'nom':user.nom,
                'matricule':user.matricule,
                'email':user.email,
                'role':user.role
                }

            flash('Welcome %s' % user.nom)

            return redirect(url_for('data_lib.index'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form,user=user)



@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():

    # If sign in form is submitted
    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        #register user
    
        user = User(nom=form.nom.data,email=form.email.data,password=generate_password_hash(form.password.data),matricule=form.matricule.data)
    
        db.session.add(user)
        db.session.commit()
    
        flash('Thanks for registering')
    
        return redirect(url_for('auth.signin',message="success"))

    return render_template("auth/signup.html", form=form)

@mod_auth.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    
    return redirect(url_for('auth.signin'))
