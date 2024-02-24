from app import app
from utils.validation import validate_debug_mode
from configuration.config import get_port


def run_app(configured_app, port=None, debug_mode=None):
    """
    Run the Flask application.

    Args:
        configured_app (Flask): The configured Flask application instance.
        port (int): The port number on which the application will run.
        Defaults to the value of the PORT environment variable.
        debug_mode (bool): Whether to run the application in debug mode.
        Defaults to the value of the DEBUG environment variable.

    Returns:
        None

    Raises:
        None
    """
    debug_mode = validate_debug_mode(debug_mode)

    port = port if port is not None else get_port()

    configured_app.run(debug=debug_mode, port=port)


if __name__ == "__main__":
    run_app(app)
