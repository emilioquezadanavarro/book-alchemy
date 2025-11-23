# Import section
from flask import Flask, request, render_template, flash, redirect, url_for
import os
from data_models import db, Author, Book
from datetime import datetime


""" 🏗️ Setup """
# 1. Initialize the Flask Application
app = Flask(__name__)

# 2. Setting up routes

@app.route('/')
def home():
    # Retrieve sort_by parameter (default: title)
    sort_by = request.args.get('sort_by', 'title')
    search_term = request.args.get('search_term')

    # Built the base query (not executed yet )
    query = Book.query.join(Author)

    # Applying search filter
    if search_term:
        # Wildcard format
        search_pattern = f"%{search_term}%"
        query = query.filter(Book.title.ilike(search_pattern))

    # Applying conditional sort
    if sort_by == 'author':
        query = query.order_by(Author.name)
    elif sort_by == "title":
        query = query.order_by(Book.title)

    # Execute final query
    all_books = query.all()

    if search_term and not all_books:

        # User searched, but the list of results is empty
        flash(f"No books found matching '{search_term}'. Showing all books.", 'warning')

        # Reset the book list if not results were found, so the user sees the list
        # instead of a blank page.
        all_books = Book.query.join(Author).order_by(Book.title).all()

    elif search_term and all_books:
        flash(f"Showing results for '{search_term}'.", 'success')


    return render_template('home.html', books=all_books)


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
            flash(f"The author '{name}' was successfully added")

            # Redirect the user to the GET Route
            return redirect(url_for('add_author'))

        else:
            # One or more fields are missing - display error
            flash('All fields are mandatory.', 'error')
            return redirect(url_for('add_author'))


    # Handle GET or finished POST (Default action: show the form)
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        # Getting data from add_book.html
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')


        # Validation all fields are filled
        if isbn and title and publication_year and author_id:

            # Convert publication_year to an integer
            publication_year = int(publication_year)

            # Convert author_id to an integer
            author_id = int(author_id)

            new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

            # Adding new author to database
            db.session.add(new_book)

            # Commit the changes
            db.session.commit()

            # Success message using flash function
            flash(f"The book called '{title}', was successfully added")

            # Redirect the user to the GET Route
            return redirect(url_for('add_book'))

        else:
            # One or more fields are missing - display error
            flash('All fields are mandatory.', 'error')
            return redirect(url_for('add_book'))

    authors = Author.query.all()

    # Handle GET or finished POST (Default action: show the form)
    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>/delete', methods = ['POST'])
def delete_book(book_id):

    # Find the book with matching ID
    book_to_delete = Book.query.get(book_id)

    if book_to_delete:

        # Get the Author object before deleting the book
        author_to_check = book_to_delete.author

        # Stage for deletion
        db.session.delete(book_to_delete)

        # Check if the author's list is now empty
        if not author_to_check.books:
            # Stage the author for deletion and flash message
            db.session.delete(author_to_check)
            flash_message = f"Book '{book_to_delete.title}' and author '{author_to_check.name}' deleted successfully!"
        else:
            flash_message = f"Book '{book_to_delete.title}' deleted successfully!"

        # Commit changes
        db.session.commit()

        # Flash message and redirect
        flash(flash_message, 'success')
        return redirect(url_for('home'))

    else:
        flash("Book not found", 'error')
        return redirect(url_for('home'))


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