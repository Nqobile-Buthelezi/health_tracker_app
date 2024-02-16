from app import app


def run_app():
    """Runs the Flask application."""
    app.run(debug=True)  # You can adjust debug mode as needed


if __name__ == "__main__":
    run_app()
