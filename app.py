from flask import Flask, render_template

app = Flask(__name__)


# Define routes and views
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/exercise_tracking")
def login():
    return render_template("exercise_tracking.html")


if __name__ == "__main__":
    app.run(debug=True)
