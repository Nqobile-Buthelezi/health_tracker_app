from flask import render_template, request, redirect
from app import app, db
from app.forms import SignupForm, LoginForm
from app.models import User
import bcrypt


# Define routes and views – this is where the rendering and redirecting happens for our users
@app.route("/")
def index():
    """ This renders the homepage, to keep the home route simple. """
    # Loads up our base template as a defining structure along with our index.html
    return render_template("base/index.html")


# @app.route("/signup", methods=["GET", "POST"])
# def sign_up():
#     """ Handles sign-up logic. GET shows the form, POST does the database and collecting work. """
#     if request.method == "POST":
#         # Extract what the user typed into the form
#         username = request.form.get("username")
#         email = request.form.get("email")
#         password = request.form.get("password")
#
#         # Let's make a new User & fill it with their info
#         new_user = User(username=username, email=email, password=password)
#
#         # Add the new user into the database using SQLAlchemy.
#         db.session.add(new_user)
#         db.session.commit()
#
#         # Ask user to log in with newly saved credentials
#         return redirect("/login")
#
#     # If they just visited the page, give them the sign-up form
#     return render_template("auth/signup.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#
#         # (VERY INSECURE) Example check
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             # Successful login (you'd usually track this with sessions. will implement later)
#             return redirect("/")  # Some page after login
#         else:
#             # Failed login
#             return render_template("auth/login.html", error="Invalid credentials")
#
#     return render_template("auth/login.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """ Handles sign-up logic using Flask WTForms. GET shows the form, POST does the database and collecting work. """
    form = SignupForm()
    if form.validate_on_submit():  # Handles validation
        # Hash and Slat for encryption purposes
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())

        # Let's make a new User & fill it with their info
        new_user = User(username=form.username.data, email=form.email, password=hashed_password)

        # Add the new user into the database using SQLAlchemy.
        db.session.add(new_user)
        db.session.commit()

        # Ask user to log in with newly saved credentials
        return redirect("/login")

    # If they just visited the page, this renders the sign-up form
    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Successful login!  (Do your logged-in user stuff)
            return redirect("/dashboard")
        else:
            # Failed login: display an error message
            return render_template("auth/login.html", form=form, error="Invalid credentials")


# Render simple html pages section
@app.route("/exercise_tracking")
def exercise_tracking():
    return render_template("features/exercise_tracking.html")


@app.route("/download")
def download():
    return render_template("download.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
