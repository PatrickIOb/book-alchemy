📚 Book Alchemy

A minimalistic Flask web application for managing books & authors — search, sort, and curate your own digital library.

✨ Overview

Book Alchemy is a lightweight Flask application that lets you manage books and authors inside a personal library database.
It provides a clean, modern, dark-themed interface to:

Add books

Add authors

Browse books in a gallery view

Sort books by title, author, or publication year

Search books by keyword

Delete books (with optional automatic cleanup of authors)

All data is stored in a local SQLite database using SQLAlchemy ORM.

The project is perfect as a beginner-to-intermediate practice app for:

Flask routing & forms

SQLAlchemy models & relationships

CRUD operations

Templating with Jinja2

Dark mode UI styling

Organizing a multi-page Flask project


🛠 Technologies Used
```
Component	        Purpose
Python 3.x	        Main programming language
Flask	                Web framework
Flask-SQLAlchemy	ORM & database integration
SQLite	                Lightweight database backend
Jinja2	                HTML templating
HTML5 + CSS3	        UI & styling
OpenLibrary Covers API	Book cover images via ISBN
```

📁 Project Structure
```
project/
│ app.py
│ data_models.py
│ README.md
│
├─ data/
│    library.sqlite        # database file
│
├─ templates/
│    home.html
│    add_book.html
│    add_author.html
│
└─ static/
     style.css
```

🚀 Features
✔ Add Authors

Name

Birth date

Death date (optional)

✔ Add Books

ISBN

Title

Publication year

Assign to existing author

Automatic cover lookup via ISBN


✔ Sorting

Sort by title, author name, or publication year

Ascending / descending


✔ Keyword Search

Search book titles

Search author names

Partial & case-insensitive matching (LIKE / ILIKE)


✔ Deleting Books

Delete a book with one click

If the book's author has no other books → delete author automatically

Feedback through Flask's flash() system


✔ Modern Gallery UI

Responsive grid layout

Elegant dark design

Styled buttons, cards, and forms

Navigation bar for quick access


🧩 Data Models

Author
```
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)
```

Book
```
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship("Author", backref="books")
```

🖥 Running the App
1. Install dependencies
```
pip install flask flask_sqlalchemy
```

2. Create the database

Uncomment the following lines in app.py and run the app once:
```
with app.app_context():
    db.create_all()
```

Then comment them out again.

3. Start the server
```
python app.py
```

Flask will run on:

http://127.0.0.1:5000/


🔧 Configuration

If you modify database location, adjust this line in app.py:
```
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/library.sqlite"
```

🧹 Deleting Books

When deleting a book:

The app removes the book

Checks if the author has any books left

If not → deletes the author as well

All actions provide feedback via flash() messages


📦 Sample Data

You can seed sample authors & books to quickly test the UI.


📜 License

This project is free to use for educational and personal purposes.


💡 Future Improvements (Ideas)

Edit / update books & authors

Pagination for large libraries

Cover caching

User accounts & login

Export library to CSV / JSON

