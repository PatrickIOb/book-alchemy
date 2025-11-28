"""
Database models for the Book Alchemy application.

Defines the SQLAlchemy models:
- Author: representing book authors
- Book: representing books and linking to authors
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Database model representing an author."""

    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author id={self.id} name={self.name!r}>"

    def __str__(self):
        if self.date_of_death:
            return f"{self.name} ({self.birth_date} – {self.date_of_death})"
        return f"{self.name} (b. {self.birth_date})"


class Book(db.Model):
    """Database model representing a book."""

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.id"),
        nullable=False,
    )

    # Relationship helper
    author = db.relationship("Author", backref="books")

    def __repr__(self):
        return f"<Book id={self.id} title={self.title!r}>"

    def __str__(self):
        if self.author:
            return f"{self.title} ({self.author})"
        return self.title