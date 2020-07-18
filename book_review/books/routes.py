from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import current_user, login_required
from book_review import db
from book_review.models import Book
from book_review.books.forms import SearchForm


books = Blueprint("books", __name__)


@books.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if request.method == "POST":
        searchText = "%" + form.searchText.data + "%"
        results = Book.query.filter((Book.isbn.like(searchText)) | (Book.title.like(searchText)) | (Book.author.like(searchText))
        ).all()
        if len(results) == 0:
            msg = (
                "We can't find any match. Please try with other Title, Author or ISBN!"
            )
            return jsonify({"success": False, "msg": msg})

        books_list = [book.toJson() for book in results]
        return jsonify({"success": True, "books_list": books_list})

    return render_template("search.html", title="Search", form=form)


@books.route("/book/<int:book_id>", methods=["GET", "POST"])
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", title="Book Details", book=book)

