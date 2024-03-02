import unittest
from app import app, db
from app.user_model import User
from sqlalchemy import inspect


class TestDatabaseManagement(unittest.TestCase):

    def setUp(self):
        """Set's up our test environment."""
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Creates any necessary tables or data.
        db.create_all()

        # Add user
        self.add_user()

    def tearDown(self):
        """'Tear's down the testing apparatus or environment."""
        # Clean up the resources.
        db.session.remove()
        # Remove any tables and data within the database.
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def add_user():
        """Adds one user to the database."""
        user = User(username="test_user_one", email="test_one@example.co.za", password="my_hashed_password")
        db.session.add(user)
        db.session.commit()

        # Commit the changes to the database
        db.session.commit()

    def test_existing_data(self):
        """Tests if there are currently users in the database."""
        # Queries the database for existing user data.
        user_count = db.session.query(User).count()
        # Assert the number of values in the database is one.
        self.assertEqual(user_count, 1)

    def test_drop_all_tables(self):
        """Test dropping all tables from the database."""
        # Before dropping the data, checks if the users table exists and inspects it's structure
        pre_inspector = inspect(db.engine)
        tables_before_drop = pre_inspector.get_table_names()
        # Assert that user table exists
        self.assertIn("users", tables_before_drop)

        # Execute drop all and delete all data from the database
        db.drop_all()

        # Inspect the database after dropping all tables
        post_inspector = inspect(db.engine)

        # Query the database to check that all tables have been dropped.
        tables_after_drop = post_inspector.get_table_names()
        # Assert that the 'users' table no longer exists.
        self.assertNotIn("users", tables_after_drop)

    def test_create_all_tables(self):
        """Test creating all tables in the database."""
        # Query the database to verify that all expected tables have been created
        inspector = inspect(db.engine)
        tables_after_create = inspector.get_table_names()
        # Assert that 'users' table is present
        self.assertIn('users', tables_after_create)
