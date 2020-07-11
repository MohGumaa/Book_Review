import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from book_review import app, db, bcrypt
from book_review.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm
from book_review.models import User, Book, Review
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POSt"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hash_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POSt"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static", "profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POSt"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            # Add code to remove old img
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", form=form, image_file=image_file
    )


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if request.method == "POST":
        searchText = "%" + form.searchText.data + "%"
        results = Book.query.filter(
            (Book.isbn.like(searchText))
            | (Book.title.like(searchText))
            | (Book.author.like(searchText))
        ).all()
        if len(results) == 0:
            msg = (
                "We can't find any match. Please try with other Title, Author or ISBN!"
            )
            return jsonify({"success": False, "msg": msg})

        books_list = [book.toJson() for book in results]
        return jsonify({"success": True, "books_list": books_list})

    return render_template("search.html", title="Search", form=form)


@app.route("/book/<int:book_id>", methods=["GET", "POST"])
@login_required
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", title="Book Details", book=book)
