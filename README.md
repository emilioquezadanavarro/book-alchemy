# 📚 Digital Library Management System

This project is a full-stack web application built using the Flask framework and Flask-SQLAlchemy, designed to manage a personal digital library of books and their authors. It demonstrates core web development concepts, including data modeling, form handling, ORM (Object-Relational Mapping) persistence, and complex querying.

# ✨ Features

This application implements the following key functionalities:

Full CRUD Functionality: Supports creation and reading of all records.

Data Modeling: Uses a One-to-Many relationship between Author and Book models (Foreign Key).

Search: Allows users to search the library by book title using case-insensitive wildcard filtering (ILIKE).

Sorting: Enables sorting of the home page book list by both Title and Author Name via URL parameters.

Robust Deletion: Deleting a book automatically checks if the corresponding author has any remaining books; if not, the author record is also deleted (cascading cleanup).

Form Handling: Implements the Post/Redirect/Get (PRG) pattern for clean form submissions and uses Flask's flash() mechanism for user feedback.


# 🛠️ Technology Stack

Backend Framework: Python / Flask

Database ORM: Flask-SQLAlchemy

Database: SQLite3 (library.sqlite)

Templating: Jinja2

Styling: Custom CSS (External Stylesheet)

📁 Project Structure

**Root Files:**
- `app.py` - Main Flask application, routes, and logic
- `data_models` - SQLAlchemy ORM model definitions
- `.gitignore` - Git ignore rules
- `README.md` - This file

**Folders:**
- `static/` - Static assets
  - `style.css` - Custom styling
- `templates/` - HTML templates
  - `home.html` - Homepage
  - `add_author.html` - Form for adding a new author
  - `add_book.html` - Form for adding a new book (with Author dropdown)
- `data` - Storage database
  - `library.sqlite` - The main SQLite database file (It will be created the first time you run the app)

# 🚀 Setup and Running Locally

1. Prerequisites

Ensure you have Python 3.x installed.

2. Installation

Clone the Repository:

git clone https://github.com/emilioquezadanavarro/book-alchemy.git


Install Dependencies:

pip install Flask , Flask-SQLAlchemy


3. Database Initialization

The database schema must be created before the application can run.

Create the Database File:

Run the Creation Script: Ensure the create_database_tables() function call is uncommented in app.py's if __name__ == "__main__": block.

python app.py


Stop the server immediately after running.

Final Setup: Comment out the create_database_tables() call to prevent tables from being recreated on subsequent runs.

4. Running the Application

python app.py


The application will be accessible at http://127.0.0.1:5000/.

# ⚙️ Key Database Concepts

This project relies heavily on Flask-SQLAlchemy's Object-Relational Mapping (ORM) capabilities:

- db.Model: (Found in data_models.py) All data classes inherit from this base class, transforming Python classes into database tables.

- db.relationship(): (Found in data_models.py) Explicitly defines the connection between the Book (many) and Author (one) models, which is necessary to enable direct attribute access like book.author.name in the template.

- Book.query.get(id): (Found in app.py) Used for highly efficient, primary key lookup when fetching a single record (like a book to be deleted).

- .filter(Book.title.ilike('%term%')): (Found in app.py) Implements the core search functionality, enabling case-insensitive wildcard searches against the book title.

- .join(Author).order_by(Author.name): (Found in app.py) Executes a complex query that links two tables and sorts the resulting book list based on the author's name from the joined table.

# 🔗 Application Routes

The application exposes the following endpoints:

- / (GET): The homepage. This route displays the entire library list and handles URL parameters for both Sorting (by title or author) and Searching.

- /add_author (GET / POST): Handles displaying the author form (GET) and processing form data to create a new Author record in the database (POST).

- /add_book (GET / POST): Handles displaying the book form, pre-populated with a dropdown list of existing authors (GET), and processes the data to save a new Book record (POST).

- /book/<int:book_id>/delete (POST): A secure, POST-only route responsible for deleting a specific book record. It includes robust logic to check if the book's author has any remaining books, deleting the author if their list becomes empty.

# 🚀 Future Enhancements

- Use ChatGPT to Redesign the UI
- Detail Pages
- Book Ratings

## 📄 License

This project is open-source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements!

HAPPY READING 📚 !

