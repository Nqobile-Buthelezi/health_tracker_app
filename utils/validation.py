import os


def validate_debug_mode(debug_mode):
    """
    Validates the debug mode supplied is a boolean value and subsequently checks if the value is true or false
    :param debug_mode:
    :return: boolean (debug_mode) - the mode we will use to start the app
    """
    # Convert debug_mode to boolean
    if debug_mode is not None:
        if isinstance(debug_mode, bool):
            debug_mode = debug_mode
        elif isinstance(debug_mode, str):
            if debug_mode.lower() in ("true", "yes", "1"):
                debug_mode = True
            elif debug_mode.lower() in ("false", "no", "0"):
                debug_mode = False
            else:
                raise ValueError("Invalid value for debug_mode. Must be a boolean or a string representing a boolean.")
        else:
            raise ValueError("Invalid value for debug_mode. Must be a boolean or a string representing a boolean.")
    else:
        environ_debug = os.getenv("DEBUG", "True")
        # Set default to True if not set
        debug_mode = (environ_debug.lower() in ("true", "yes", "1")) if environ_debug != "" else True

    return debug_mode
