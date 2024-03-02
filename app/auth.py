from datetime import datetime

from flask import Blueprint, render_template, redirect, flash, url_for, session, make_response
from app import db
from app.signup_form import SignupForm
from app.login_form import LoginForm
from app.user_model import User
import bcrypt

authentication_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@authentication_blueprint.route("/signup", methods=["GET"])
def display_signup_form():
    """Displays the signup form."""
    form = SignupForm()
    return render_template("auth/signup.html", form=form)


@authentication_blueprint.route("/signup", methods=["POST"])
def process_signup_form():
    """Processes form data, creates a new user account, and redirects to log in on success."""
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match.", category="error")
            return redirect(url_for("auth.sign_up"), code=302)

        if User.query.filter_by(email=form.email.data).first():
            flash("A user with that email already exists. Please try again.", category="error")
            return redirect(url_for("auth.sign_up"), code=302)

        if User.query.filter_by(username=form.username.data).first():
            flash("That username is taken. Please choose another.", category="error")
            return redirect(url_for("auth.display_signup_form"), code=302)

        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", category="success")
        return redirect(url_for("auth.display_login_form"))
    else:  # Validation failed
        flash("Validation failed. Please try again.", category="error")
        return redirect(url_for("auth.display_signup_form"), code=302)


@authentication_blueprint.route('/login', methods=["GET"])
def display_login_form():
    """Displays the login form."""
    form = LoginForm()
    return render_template("auth/login.html", form=form)


@authentication_blueprint.route('/login', methods=["POST"])
def login_user():
    """Authenticates user credentials and redirects on success."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password_hash.encode('utf-8')):
            # Update session with user ID
            session['user_id'] = user.id
            # Update user's last login timestamp
            user.last_login = datetime.utcnow()
            db.session.commit()
            # Successful login
            # flash("Login successful!", category="success")
            return redirect(url_for("main.index"))  # Replace 'index' if needed
        else:
            error = "Incorrect username or password."
            flash(error, category="error")
            return render_template("auth/login.html", form=form), 401

    return make_response(render_template("auth/login.html"), 200)
