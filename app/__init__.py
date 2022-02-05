# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Define the WSGI application object
app = Flask(__name__,static_url_path='',static_folder='static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',error=error), 500

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_book.controllers import mod_book as book_module
from app.main.routes import main as main_module
# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(main_module)
app.register_blueprint(book_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()