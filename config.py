#from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from app.models import Book

'''Flask: framework webowy, który używamy do tworzenia aplikacji webowej.
request: moduł Flask używany do obsługi żądań HTTP.
jsonify: moduł Flask, który konwertuje dane Python do formatu JSON.
SQLAlchemy: ORM (Object Relational Mapper) do interakcji z bazą danych w sposób obiektowy.'''

class Config:
    #app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    #db = SQLAlchemy(app)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'

'''Tworzymy instancję aplikacji Flask.
Konfigurujemy URI bazy danych, używając SQLite (sqlite:///books.db). Oznacza to, że baza danych zostanie zapisana w pliku books.db.
Inicjalizujemy obiekt SQLAlchemy, który będzie odpowiadał za interakcję z bazą danych.'''
