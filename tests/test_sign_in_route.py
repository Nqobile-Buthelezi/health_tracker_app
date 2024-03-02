import unittest
from app import app, db, User


class TestSignUpRoute(unittest.TestCase):

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

    def tearDown(self):
        """'Tears' down the test, will implement logic later."""
        self.app_context.pop()

    def test_signup_route_get(self):
        """Tests the 'auth/signup' route's GET request to render the signup page."""
        response = self.client.get("/auth/signup")
        self.assertEqual(200, response.status_code)

    def test_signup_with_valid_data(self):
        """Tests the 'auth/signup' route's POST request with valid form data."""
        post_response = self.client.post("/auth/signup", data=dict(
            username="new_user",
            email="new_test@email.com",
            password="password123",
            confirm_password="password123"
        ), follow_redirects=True)

        self.assertEqual(post_response.status_code, 200)

    def test_signup_with_invalid_password_confirmation(self):
        """Tests the 'auth/signup' route's POST request with invalid password confirmation."""
        post_response = self.client.post("/auth/signup", data=dict(
            username="new_user",
            email="new_test@email.com",
            password="password123",
            confirm_password="password456"  # Incorrect confirmation password
        ), follow_redirects=True)

        self.assertEqual(post_response.status_code, 200)

        # Assert that a new user has not been added to the users' database.
        new_user = User.query.filter_by(username="new_user").first()
        self.assertIsNone(new_user)

    def test_signin_route_get(self):
        """Tests our 'auth/signup' route's get request to the page"""
        # Test GET request.
        get_response = self.client.get("auth/signup")
        self.assertEqual(200, get_response.status_code)

    def test_signin_route_post(self):
        """Tests our 'auth/signup route's POST request for posting data to the form."""
        # Test POST request with valid form data.
        post_response = self.client.post("auth/signup", data=dict(
            username="new_user",
            email="new_test@email.com",
            password="password123",
            confirm_password="password123"
        ), follow_redirects=True)

        # Assert that the post requests status code is OK.
        self.assertEqual(post_response.status_code, 200)

        # Assert that a new user has been added to the users' database.
        new_user = User.query.filter_by(username="new_user").first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, "new_test@email.com")


if __name__ == '__main__':
    unittest.main()
