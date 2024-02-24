import unittest
from app import app, db


class TestAppInitialisation(unittest.TestCase):

    def test_configuration(self):
        """Tests if the configured application's configuration data is not empty."""
        self.assertIsNotNone(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertIsNotNone(app.config["SECRET_KEY"])

    def test_database_initialisation(self):
        """Tests if the applications database is created and configured."""
        self.assertIsNotNone(db)

        with app.app_context():
            # Check if the database engine is created
            self.assertIsNotNone(db.engine)

            # Check if the database engine is an instance of SQLAlchemy's Engine class
            from sqlalchemy.engine.base import Engine
            self.assertIsInstance(db.engine, Engine)

    def test_user_table_columns(self):
        """Tests if the "user" table has the correct columns within it."""
        # Establish a connection to the database
        with app.app_context():
            # With the assumption that "users" is the name of your table
            metadata = db.metadata
            user_table = metadata.tables.get("users")

            # Check that the users table actually exists
            self.assertIsNotNone(user_table)

            # Assert correct columns names are present
            self.assertIn("id", user_table.columns)
            self.assertIn("username", user_table.columns)
            self.assertIn("email", user_table.columns)
            self.assertIn("password_hash", user_table.columns)

    def test_import_user(self):
        """Tests the use case of importing the User class."""
        from app.user_model import User
        self.assertIsNotNone(User)

    def test_template_blueprint_registration(self):
        """Tests if the auth blueprint was successfully registered."""
        # Print the registered blueprints for debugging
        print([(bp.name, bp.url_prefix) for bp in app.blueprints.values()])

        # Check if any blueprint has the expected URL prefix
        self.assertTrue(any(bp.url_prefix == "/auth" for bp in app.blueprints.values()))

    def test_import_routes(self):
        """Tests if the routes are imported successfully."""
        with app.test_request_context():
            self.assertIsNotNone(app.url_map.bind(""))
