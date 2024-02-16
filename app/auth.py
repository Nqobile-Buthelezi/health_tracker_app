from flask import Blueprint, render_template, redirect, flash, url_for
from app import db
from app.signup_form import SignupForm
from app.login_form import LoginForm
from app.user_model import User
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def sign_up():
    """Handles user signup logic.

    GET request: Displays the signup form.
    POST request: Processes form data, creates a new user account, and redirects
                  to log in on success.
    """

    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match.", category="error")
            return render_template("auth/signup.html", form=form)

        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)

        # Check for existing users to prevent duplicates (you might extend this)
        if User.query.filter_by(email=form.email.data).first():
            flash("A user with that email already exists. Please try again.", category="error")
            return render_template("auth/signup.html", form=form)

        if User.query.filter_by(username=form.username.data).first():
            flash("That username is taken. Please choose another.", category="error")
            return render_template("auth/signup.html", form=form)

        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", category="success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login.

    GET request: Displays the login form.
    POST request: Authenticates user credentials and redirects to the protected
                  dashboard on success.
    """

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            # Successful login (Implement session management here)
            flash("Login successful!", category="success")
            return redirect(url_for("index"))  # Replace 'index' if needed
        else:
            error = "Incorrect username or password."
            flash(error, category="error")
            return render_template("auth/login.html", form=form, error=error)

    return render_template("auth/login.html", form=form)
