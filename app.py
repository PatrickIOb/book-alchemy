import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from data_models import Author, Book, db

app = Flask(__name__)
app.secret_key = "first-timer"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Connect the app with the database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'data/library.sqlite')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the db extension
db.init_app(app)


@app.route("/")
def index():
    """
    Show all books and allow sorting by author, title, or year
    in ascending or descending order. Supports a simple search.
    """
    # Sort: title, author, year
    sort = request.args.get("sort", "title")
    # Order: asc or desc
    order = request.args.get("order", "asc")
    # Search query
    q = request.args.get("q", "").strip()

    # Base query: join author to book table so we can sort by author.name
    query = Book.query.join(Author)

    if q:
        like_pattern = f"%{q}%"
        query = query.filter(
            or_(
                Book.title.ilike(like_pattern),
                Author.name.ilike(like_pattern),
            )
        )

    # Choose column to sort
    if sort == "author":
        sort_column = Author.name
    elif sort == "year":
        sort_column = Book.publication_year
    else:
        # Default: sort by title
        sort = "title"
        sort_column = Book.title

    # Descending or ascending
    if order == "desc":
        books = query.order_by(sort_column.desc()).all()
    else:
        order = "asc"  # Fallback
        books = query.order_by(sort_column.asc()).all()

    return render_template(
        "home.html",
        books=books,
        sort=sort,
        order=order,
        q=q,
    )


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """POST adds a new author, GET shows the form."""
    message = None

    if request.method == "POST":
        name = request.form["name"]

        # Birth date parsing to datetime.date
        birthdate_str = request.form.get("birth_date")
        birth_date = datetime.strptime(birthdate_str, "%Y-%m-%d").date()

        # Death date may be empty
        death_str = request.form.get("date_of_death", "").strip()
        if death_str:
            date_of_death = datetime.strptime(death_str, "%Y-%m-%d").date()
        else:
            date_of_death = None

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death,
        )

        db.session.add(new_author)
        db.session.commit()

        message = f"Author {name} added successfully"

    return render_template("add_author.html", message=message)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """POST adds a new book, GET shows the form."""
    message = None

    # Load all authors from the database
    authors = Author.query.all()

    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        publication_year = request.form["publication_year"]
        author_id = request.form["author_id"]

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id,
        )

        db.session.add(new_book)
        db.session.commit()

        message = f"Book {new_book.title} added successfully"

    return render_template("add_book.html", message=message, authors=authors)


@app.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    """Delete a book and optionally its author if no books remain."""
    book = Book.query.get(book_id)

    if not book:
        flash("Error: Book not found.", "error")
        return redirect(url_for("index"))

    # Save details for message
    title = book.title
    author = book.author

    # Delete book
    db.session.delete(book)
    db.session.commit()

    # Check if author has another book
    remaining_books = Book.query.filter_by(author_id=author.id).count()

    if remaining_books == 0:
        # If author has no remaining book -> delete author
        author_name = author.name
        db.session.delete(author)
        db.session.commit()
        flash(
            (
                f"Book '{title}' deleted and author '{author_name}' removed "
                "(no more books left)."
            ),
            "success",
        )
    else:
        flash(f"Book '{title}' deleted successfully.", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    # Use this once to create tables:
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)