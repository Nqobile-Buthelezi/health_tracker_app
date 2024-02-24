import os
import unittest
from unittest.mock import patch
from app import app
from run import run_app


class TestRunApp(unittest.TestCase):

    def test_run_app_default_config(self):
        """Tests if the application runs with default configuration."""
        with patch("app.app.run") as mock_run:
            run_app(app)
            mock_run.assert_called_once_with(debug=True, port=5500)

    def test_run_app_custom_config(self):
        """Tests if the application runs with custom configuration."""
        with patch("app.app.run") as mock_run:
            run_app(app, port=8080, debug_mode=False)
            mock_run.assert_called_once_with(debug=False, port=8080)

    def test_run_app_if_port_invalid_type(self):
        """Tests if the application throws an error if the port is invalid."""
        with self.assertRaises(ValueError):
            run_app(app, port="invalid port", debug_mode=False)

    def test_run_app_if_debug_mode_invalid_type(self):
        """Tests if the application throws an error if the debug mode is not a boolean."""
        with self.assertRaises(ValueError):
            run_app(app, port=7000, debug_mode="invalid debug mode")

    @patch.dict(os.environ, {"PORT": "", "DEBUG": ""})
    def test_run_app_with_default_environment_variables(self):
        """Tests if the application runs with default values if environmental variables are not set."""
        with patch("app.app.run") as mock_run:
            run_app(app)
            mock_run.assert_called_once_with(debug=True, port=5000)

    def test_run_app_maximum_port_value(self):
        """Tests if the application runs with the maximum value for the port and a False values for debug mode."""
        with patch("app.app.run") as mock_run:
            run_app(app, port=65535, debug_mode=False)
            mock_run.assert_called_once_with(port=65535, debug=False)

    def test_run_app_minimum_port_value(self):
        """Tests if the application runs with the minimum value possible and debug mode set to True."""
        with patch("app.app.run") as mock_run:
            run_app(app, port=0, debug_mode=True)
            mock_run.assert_called_once_with(port=0, debug=True)

    def test_run_app_extreme_port_value(self):
        """Tests if the application runs with an extreme value for the port and debug mode set to None"""
        with patch("app.app.run") as mock_run:
            run_app(app, port=1000000, debug_mode=None)
            mock_run.assert_called_once_with(port=1000000, debug=True)
