# Book Alchemy -- Flask Web App

Eine minimalistische Flask-Anwendung zur Verwaltung von Büchern und
Autoren, inklusive Sortierfunktion, Suchfunktion und Galerieansicht.
Perfekt geeignet als Lernprojekt oder Basis für größere Webanwendungen
mit CRUD-Features.

## Features

-   Bücher hinzufügen, anzeigen, durchsuchen und löschen
-   Autoren hinzufügen (inkl. Geburtsdatum und optionalem Sterbedatum)
-   Sortierung nach Titel, Autor oder Erscheinungsjahr (`asc` oder
    `desc`)
-   Keyword-Suche über Buchtitel und Autorennamen
-   Automatisches Entfernen eines Autors, wenn keine Bücher mehr
    vorhanden sind
-   Dunkles, modernes UI im Galerie-Layout
-   Saubere Strukturierung mit Flask, SQLAlchemy und Jinja2

## Projektstruktur

``` bash
book-alchemy/
├── app.py
├── data_models.py
├── README.md
│
├── data/
│   └── library.sqlite
│
├── templates/
│   ├── home.html
│   ├── add_book.html
│   └── add_author.html
│
└── static/
    └── style.css
```

## Installation

``` bash
# Repository klonen
git clone https://github.com/PatrickIOb/book-alchemy.git
cd book-alchemy

# Virtuelle Umgebung erstellen (optional)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install flask flask_sqlalchemy
```

## Datenbank initialisieren

``` python
with app.app_context():
    db.create_all()
```

Einmal ausführen, um die `library.sqlite` in `data/` anzulegen.\
Danach wieder auskommentieren.

## Starten der Anwendung

``` bash
    python app.py
```

Die App ist dann erreichbar unter:

    http://localhost:5000/

## Beispiel-Funktionalität

### Startseite `/`

Listet alle Bücher in einer Galerieansicht auf.

#### Query-Parameter

-   `sort=title|author|year`
-   `order=asc|desc`
-   `q=<suchbegriff>`

#### Beispiele

``` bash
    # Sortierung nach Autor absteigend
    http://localhost:5000/?sort=author&order=desc
    
    # Sortierung nach Erscheinungsjahr aufsteigend
    http://localhost:5000/?sort=year&order=asc
    
    # Suche nach "ring" im Titel oder Autor
    http://localhost:5000/?q=ring
```

## Beispielhafte Datenmodelle

### Author

``` python
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)
```

### Book

``` python
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship("Author", backref="books")
```

## Lizenz

MIT License -- frei zur Nutzung, Modifikation und Verteilung.