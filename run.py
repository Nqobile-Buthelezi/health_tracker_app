from app import app, db

# Important for SQLAlchemy to work nicely
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    # Execute our app while we can see live changes,
    # and errors in realtime in the console
    app.run(debug=True)
