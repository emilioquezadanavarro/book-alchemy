# Import and create a db object:
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Defining Class
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Authors(id = {self.id}, name = {self.name})"

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return f"Books(id = {self.id}, name = {self.title})"

