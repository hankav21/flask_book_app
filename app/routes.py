
#from flask_sqlalchemy import SQLAlchemy

import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash, session
from app import app, db
from app.models import Book, Reader, Borrow




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
    borrows = Borrow.query.all()
    return render_template('index.html', books=books, readers=readers, borrows=borrows)

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
    search_query = request.args.get('search')
    if search_query:
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
        
    else:
        books = Book.query.all()  # Pobierz wszystkie książki z bazy danych
     
    return render_template('browse.html', books=books)  # Przekaż książki do szablonu

# @app.route('/borrow/<int:book_id>', methods=['GET','POST'])
# def borrow_book(book_id):
#     if 'logged_in_user' in session:
#         reader_id = session['logged_in_user']
#         borrow_date = datetime.datetime.now()
#         new_borrow = Borrow(book_id=book_id, reader_id=reader_id, borrow_date=borrow_date)
#         db.session.add(new_borrow)
#         db.session.commit()
#     return redirect(url_for('browse'))

@app.route('/browse/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):   
    
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        reader_id = session.get('user_id')  # Pobranie ID aktualnie zalogowanego użytkownika z sesji
        if not reader_id:
            return jsonify({'error': 'User not logged in'}), 401
        reader = Reader.query.get(reader_id)
        if reader and not book.is_borrowed:
            borrow = Borrow(book_id=book.id, reader_id=reader_id, borrow_date=datetime.date.today())
            db.session.add(borrow)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('Book is already borrowed or invalid reader.')
    readers = Reader.query.all()
    return render_template('borrow.html', book=book, readers=readers)

# #historia wypozyczeń czytelnika
# @app.route('/borrow_history_user')
# def borrow_history_user():
    
#     return('borrow_history_user')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = Reader.query.filter_by(name=name).first()
        if user and user.password == password:
            
            session['user_name'] = user.name
            session['user_id'] = user.id
            
            flash('Login successful! Hello ' + user.name, 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password Prawidłowe hasło: ' + user.password, 'danger')
    return render_template('login.html')#funkcjonalności bibliotekarza

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

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

#usówanie czytelnika
@app.route('/delete_reader/<int:reader_id>')
def delete_reader(reader_id):
    reader = Reader.query.get(reader_id)
    db.session.delete(reader)
    db.session.commit()
    return redirect(url_for('readers'))    
