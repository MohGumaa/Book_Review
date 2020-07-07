from datetime import datetime
from book_review import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    review = db.relationship("Review", backref="user", lazy=True)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(15), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review = db.relationship("Review", backref="book", lazy=True)

    def __repr__(self):
        return f"Book ('{self.isbn}', '{self.title}', '{self.author}', '{self.year})"


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.isbn"), nullable=False)

    def __repr__(self):
        return f"Book ('{self.rating}', '{self.comment}', '{self.date_posted}')"

