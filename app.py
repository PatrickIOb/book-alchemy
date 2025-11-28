from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from data_models import db, Author, Book
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Connect the app with the Database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initilize the app with extension
db.init_app(app)

@app.route('/')
def index():
    """Show all books"""
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
    """POST adds a new author, GET gives the form to the user"""
    message=None
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form.get('date_of_death', None)

        new_author = Author(name=name,
                            birth_date=birth_date,
                            date_of_death=date_of_death)

        db.session.add(new_author)
        db.session.commit()

        message = f"Author {name} added successfully"

    return render_template("add_author.html", message=message)

@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    """POST adds a new book, GET gives the form to the user"""
    message=None
    authors = Author.query.all() #laoding all Authors from library

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

        db.session.add(new_book)
        db.session.commit()

        message = f"Book {new_book.title} added successfully"


    return render_template("add_book.html", message=message, authors=authors)


app.run(debug=True)


"""
with app.app_context():
    db.create_all()"""
