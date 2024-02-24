import os


def get_port():
    """
    Gets the port number for the flask application to run on.
    :return: int (port) - port number
    """
    environ_port = os.getenv("PORT")
    port = environ_port if environ_port != "" else 5000
    return int(port)
