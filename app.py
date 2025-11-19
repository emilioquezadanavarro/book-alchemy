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

# 4. Standard Flask Run Block
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)