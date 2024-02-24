import os
import bcrypt
from app import db


class User(db.Model):
    """Represents a user in the application's database.

    Attributes:
        __tablename__ (str): The name of the associated database table.
        id (int): The user's unique primary key identifier.
        username (str): The user's username (must be unique, max 50 characters).
        email (str): The user's email address (must be unique, max 120 characters).
        password_hash (str): The user's password (max 60 characters).
    """

    # Determine the table name based on the environment or configuration
    if os.getenv("ENVIRONMENT") == "test":
        __tablename__ = "test_users"
    else:
        __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        """Provides a developer-friendly string representation of a User object."""
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
