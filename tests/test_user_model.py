import unittest
from app import app, db, User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """Sets up the test case configuration data."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a clean database
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """'Tears' down the test, will implement logic later."""
        self.app_context.pop()

    def test_username_length_validation(self):
        """Test username length validation."""
        with self.assertRaises(ValueError):
            User(username="a" * 26, email="test@example.com", password="password123")

    def test_email_format_validation(self):
        """Tests the email validation."""
        with self.assertRaises(ValueError):
            User(username="user", email="user_email", password="password123")

    def test_set_password(self):
        """Tests if the password supplied is hashed."""
        user = User(username="test_user", email="test@example.com", password="password123")
        self.assertTrue(user.password_hash)  # Ensure the password_hash value is not empty.

    def test_check_password(self):
        """Tests if the password is correctly verified."""
        user = User(username="test_user", email="test@example.com", password="password123")

        # Verify the password
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrong_password"))
