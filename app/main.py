from flask import render_template, Blueprint


main_blueprint = Blueprint("main", __name__)


# Define routes and views – this is where the rendering and redirecting happens for our users
@main_blueprint.route("/")
def index():
    """ This renders the homepage, to keep the home route simple. """
    # Loads up our base template as a defining structure along with our index.html
    return render_template("base/index.html")


# Render simple html pages section
@main_blueprint.route("/exercise_tracking")
def exercise_tracking():
    return render_template("features/exercise_tracking.html")


@main_blueprint.route("/download")
def download():
    return render_template("download.html")


@main_blueprint.route("/about")
def about():
    return render_template("about.html")


@main_blueprint.route("/contact")
def contact():
    return render_template("contact.html")
