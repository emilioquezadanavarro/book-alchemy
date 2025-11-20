# Import section
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime


""" 🏗️ Setup """
# 1. Initialize the Flask Application
app = Flask(__name__)

# 2. Setting up routes
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    # Check the request method
    if request.method == 'POST':

        # Getting data from add_author.html
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        # Validation all fields are filled
        if name and birth_date and date_of_death:
            # Conversion to Object
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            date_of_death_obj = datetime.strptime(date_of_death, '%Y-%m-%d').date()

            new_author = Author(name=name, birth_date=birth_date_obj, date_of_death=date_of_death_obj)

            # Adding new author to database
            db.session.add(new_author)

            # Commit the changes
            db.session.commit()

            # Success message using flash function
            flash(f"Author {name} added successfully")

            # Redirect the user to the GET Route
            return redirect(url_for('add_author'))

        else:
            # One or more fields are missing - display error
            flash('All fields are mandatory.', 'error')
            return redirect(url_for('add_author'))


    # Handle GET or finished POST (Default action: show the form)
    return render_template('add_author.html')


# 3. Configure the Database Connection using absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"  # This line tells Flask-SQLAlchemy which database file to use.
app.config['SECRET_KEY'] = 'a_very_secret_key_for_flashing_messages'

# 4. Connect the Flask app to the flask-sqlalchemy code.
db.init_app(app)

# 5. Create database tables function
def create_database_tables():
    """Creates the database file and all tables defined in models."""
    print("Attempting to create database tables...")

    # db.create_all() MUST be called within the Flask Application Context
    # try/except block for robustness.
    try:

        with app.app_context():
            db.create_all()
            print("Database tables created or already exist.")
    except Exception as e:
        print(f"ERROR: Failed to create database tables. Reason: {e}")


# 6. Standard Flask Run Block
if __name__ == "__main__":

    # Call the setup function to ensure the database file and tables are ready
    # This should be run at least once to initialize the tables, then comment it out.

    #create_database_tables() # <-- Comment this line out after first successful run

    app.run(host="127.0.0.1", port=5000, debug=True)