from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    
    '''Definiujemy klasę Book, która dziedziczy po db.Model.
id, title i author to kolumny w tabeli book:
id jest kluczem głównym (primary_key=True).
title i author są kolumnami typu String z ograniczeniami długości i nie mogą być NULL (nullable=False).'''
    borrows = db.relationship('Borrow', backref='book_borrow', lazy=True)

    @property
    def is_borrowed(self):
        return any(borrow.return_date is None for borrow in self.borrows)

class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    borrows = db.relationship('Borrow', backref='reader_borrow', lazy=True)

    # def __repr__(self):
    #     return f"<Reader {self.name}>"

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    book = db.relationship('Book', backref=db.backref('borrowed_books', lazy=True))
    reader = db.relationship('Reader', backref=db.backref('borrowed_readers', lazy=True))