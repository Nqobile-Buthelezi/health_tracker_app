import os
from datetime import datetime

import bcrypt

from app import db
from sqlalchemy import func


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
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.validate_username_length(username)
        self.validate_email_format(email)
        self.is_unique_email(email)
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        """Provides a developer-friendly string representation of a User object."""
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    # Custom validation
    @staticmethod
    def validate_username_length(username):
        """Validates the length of the username."""
        if len(username) > 25:
            raise ValueError("Username must be at most 20 characters long")

    @staticmethod
    def validate_email_format(email):
        """Validates the email formate."""
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")

    @staticmethod
    def is_unique_email(email):
        """Check if the email address is unique."""
        return db.session.query(func.count(User.id)).filter_by(email=email).scalar() == 0


