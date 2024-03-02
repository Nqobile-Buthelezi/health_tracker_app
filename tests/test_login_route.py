import unittest
from app import app, db
from app.user_model import User


class TestLoginRoute(unittest.TestCase):

    def setUp(self):
        """Sets up the test case configuration data."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a clean database.
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Create a test user.
            new_user = User(username="test_user", email="test_user@email.com", password="password123")
            db.session.add(new_user)
            db.session.commit()

    def tearDown(self):
        """'Tears' down the test, will implement logic later."""
        self.app_context.pop()

    def test_login_route_get(self):
        """Tests the 'auth/login' route's GET request to render the login page."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        """Tests the 'auth/login' route's POST request with valid credentials."""
        post_response = self.client.post("auth/login", data=dict(
            username="test_user",
            password="password123"
        ), follow_redirects=True)

        self.assertEqual(post_response.status_code, 200)
        # Check user's last login timestamp in the database.
        logged_in_user = User.query.filter_by(username="test_user").first()
        self.assertIsNotNone(logged_in_user)
        self.assertIsNotNone(logged_in_user.last_login)

    def test_login_with_invalid_credentials(self):
        """Tests the 'auth/login' route's POST request with invalid credentials."""
        post_response = self.client.post("auth/login", data=dict(
            username="test_user",
            password="wrong_password"  # Incorrect password
        ), follow_redirects=True)

        self.assertNotEqual(post_response.status_code, 200)

        self.assertEqual(post_response.status_code, 401)

    def test_login_route_post(self):
        """Tests our 'auth/login' routes POST request as we attempt to simulate logging in."""
        # Create a test user.
        new_user = User(username="new_user", email="new_user@email.com", password="password123")
        db.session.add(new_user)
        db.session.commit()

        # Test POST request with valid credentials.
        post_response = self.client.post("auth/login", data=dict(
            username="new_user",
            password="password123"
        ), follow_redirects=True)

        # Assert that the requests status is OK.
        self.assertEqual(post_response.status_code, 200)

        # Check if session variable is set.
        with self.client as context:
            with context.session_transaction() as session:
                self.assertTrue(session.get("user_id") is not None)

        # Check user's last login timestamp in the database.
        logged_in_user = User.query.filter_by(username="test_user").first()
        self.assertIsNotNone(logged_in_user)
        self.assertIsNotNone(logged_in_user.last_login)


if __name__ == '__main__':
    unittest.main()
