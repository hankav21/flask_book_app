
#from flask_sqlalchemy import SQLAlchemy

import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from app import app, db
from app.models import Book, Reader#, Borrow
from app.forms import LoginForm



# @app.route('/books', methods=['POST'])
# def add_book():
#     data = request.get_json()
#     new_book = Book(title=data['title'], author=data['author'])
#     db.session.add(new_book)
#     db.session.commit()
#     return jsonify({'message': 'Book added successfully!'})
# '''Dekorator @app.route('/books', methods=['POST']) definiuje endpoint /books obsługujący żądania POST.
# request.get_json() pobiera dane JSON z żądania.
# Tworzymy nowy obiekt Book i dodajemy go do sesji db.session.add(new_book).
# Zatwierdzamy zmiany w bazie danych za pomocą db.session.commit().
# Zwracamy odpowiedź JSON potwierdzającą dodanie książki.'''


# @app.route('/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     output = []
#     for book in books:
#         book_data = {'title': book.title, 'author': book.author}
#         output.append(book_data)
#     return jsonify(output)

#app = create_app()

@app.route('/')
def index(): 
    db.create_all ()
    books = Book.query.all() #if Book.query.all() > 0 else db.create_all()
    readers = Reader.query.all() #if Reader.query.count() > 0 else [] # Dodane, aby można było wybrać czytelnika przy wypożyczaniu książki
    return render_template('index.html', books=books, readers=readers)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    new_book = Book(title=title, author=author)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))





#przegladanie przez uztkownika
@app.route('/browse')
def browse():
    books = Book.query.all()  # Pobierz wszystkie książki z bazy danych
    return render_template('browse.html', books=books)  # Przekaż książki do szablonu

# @app.route('/borrow', methods=['POST'])
# def borrow_book():
#     book_id = request.form.get('book_id')
#     reader_id = request.form.get('reader_id')
#     borrow_date = datetime.now()
#     #new_borrow = Borrow(book_id=book_id, reader_id=reader_id, borrow_date=borrow_date)
#     #db.session.add(new_borrow)
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Reader.query.filter_by(name=form.name.data).first()
        if user and user.password == form.password.data:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
#funkcjonalności bibliotekarza
@app.route('/add_reader', methods=['POST'])
def add_reader():
    name = request.form.get('name')
    password = request.form.get('password')
    new_reader = Reader(name=name, password=password)
    db.session.add(new_reader)
    db.session.commit()
    #return redirect(url_for('readers'))
    return redirect(url_for('index'))

#wyświetlanie listy czytelników
@app.route('/readers')
def readers():
    readers = Reader.query.all()
    return render_template('readers.html', readers=readers)
