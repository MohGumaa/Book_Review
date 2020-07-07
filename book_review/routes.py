from flask import render_template, url_for, flash, redirect
from book_review import app
from book_review.forms import RegistrationForm, LoginForm
from book_review.models import User, Book, Review

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POSt"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POSt"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@log.com" and form.password.data == "123":
            flash("You have been logged in!!", "success")
            return redirect(url_for("login"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)
