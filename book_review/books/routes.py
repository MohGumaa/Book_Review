import requests
import os
from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from flask_login import current_user, login_required
from book_review import db
from book_review.models import Book, Review
from book_review.books.forms import SearchForm, ReviewForm
from dotenv import load_dotenv
load_dotenv()

books = Blueprint("books", __name__)

@books.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if request.method == "POST":
        searchText = f"%{form.searchText.data}%".title()
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


@books.route("/book/<string:isbn>", methods= ['GET', 'POST'])
@login_required
def book(isbn):

    book = Book.query.filter_by(isbn=isbn).first_or_404()
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(rating=int(form.rating.data), comment=form.comment.data, user=current_user, book=book)
        db.session.add(review)
        db.session.commit()
        flash(f'Your review has been posted! {int(form.rating.data)}-{form.comment.data  }', 'success')
        return redirect(url_for("users.account"))

    """GoodReads API to get ratings_count and average_rating value"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": os.getenv("API_KEY"), "isbns": isbn}).json()["books"][0]
    ratings_count = res['work_ratings_count']
    average_rating = res['average_rating']

    # Here for star of the book from API to fill width in 100%
    starPercentage = (float(average_rating) / 5) * 100;
    starPercentageRounded = round(starPercentage / 10) * 10;

    reviews = Review.query.filter_by(book_id=isbn).all()

    return render_template("book.html", title="Book Details", form=form, book=book, ratings_count=ratings_count,
        average_rating=average_rating, starPercentage=starPercentage, starPercentageRounded=starPercentageRounded, reviews=reviews)

