from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

app.config['SECRET_KEY'] = 'wygenerowany_secret_key'  # Ustaw wygenerowany klucz

db.init_app(app)




# @app.before_request
# def before_request():
    

from app import routes, models  # Importuj routes i models na końcu, aby uniknąć cyklicznych importów

with app.app_context():
    db.create_all()
