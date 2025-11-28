from flask import Flask, request, render_template
from sqlalchemy import or_
from datetime import datetime
from data_models import db, Author, Book
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#connect the app with the database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#initilize the app with extension
db.init_app(app)

@app.route('/')
def index():
    """show all books and sort by author, title or year, in ascending or descending order"""
    sort = request.args.get('sort', 'title')   # title, author, year
    order = request.args.get('order', 'asc')   # asc oder desc
    q = request.args.get('q', '').strip() #searching term request from the query

    # base query, where we are joining the author to the book table so we can sort by author.name
    query = Book.query.join(Author)

    if q:
        like_pattern = f"%{q}%"
        query = query.filter(
            or_(
                Book.title.ilike(like_pattern),
                Author.name.ilike(like_pattern)
            )
        )

    # choose column to sort
    if sort == 'author':
        sort_column = Author.name
    elif sort == 'year':
        sort_column = Book.publication_year
    else:
        # default
        sort = 'title'
        sort_column = Book.title

    # descending or ascending
    if order == 'desc':
        books = query.order_by(sort_column.desc()).all()
    else:
        order = 'asc'  # Fallback
        books = query.order_by(sort_column.asc()).all()

    return render_template("home.html", books=books, sort=sort, order=order, q=q)

@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
    """POST adds a new author, GET gives the form to the user"""
    message=None
    if request.method == 'POST':
        name = request.form['name']
         #Birthdate parsing to datetime
        birthdate_str = request.form.get('birth_date')  # e.g. "1948-09-20"
        birth_date = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        #checking if deathdate exists and then parsing to datetime object
        death_str = request.form.get('date_of_death', "").strip()
        if death_str:
            date_of_death = datetime.strptime(death_str, "%Y-%m-%d").date()
        else:
            date_of_death = None

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
