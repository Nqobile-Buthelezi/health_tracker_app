from app import db


class User(db.Model):
    """Represents a user in the application's database.

    Attributes:
        __tablename__ (str): The name of the associated database table.
        id (int): The user's unique primary key identifier.
        username (str): The user's username (must be unique, max 50 characters).
        email (str): The user's email address (must be unique, max 120 characters).
        password (str): The user's password (max 60 characters).
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """Provides a developer-friendly string representation of a User object."""
        return f"User('{self.username}', '{self.email}')"

