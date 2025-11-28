from flask import Flask
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

"""
with app.app_context():
    db.create_all()"""

app.run(debug=True)