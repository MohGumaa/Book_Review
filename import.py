import csv

from book_review import db
from book_review.models import Book

with open("books.csv") as f:
    books = csv.reader(f)

    for isbn, title, author, year in books:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print(f"Add Book with ({isbn}: {title}, {author}, {year}) To DB.")

    db.session.commit()
