from flask import render_template
from app import app


# Define routes and views – this is where the rendering and redirecting happens for our users
@app.route("/")
def index():
    """ This renders the homepage, to keep the home route simple. """
    # Loads up our base template as a defining structure along with our index.html
    return render_template("base/index.html")


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
