from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book


""" 🏗️ Setup """
# 1. Initialize the Flask Application
app = Flask(__name__)

# 2. Configure the Database Connection using absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"  # This line tells Flask-SQLAlchemy which database file to use.

# 3. Connect the Flask app to the flask-sqlalchemy code.
db.init_app(app)

# 4. Create database tables function
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


# 4. Standard Flask Run Block
if __name__ == "__main__":
    # Call the setup function to ensure the database file and tables are ready
    # This should be run at least once to initialize the tables.
    create_database_tables()
    app.run(host="127.0.0.1", port=5000, debug=True)