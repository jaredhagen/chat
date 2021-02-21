"""
This module defines custom error handlers to generate custom error response.
"""
from werkzeug.exceptions import BadRequest, HTTPException

# for more information on flask error handling patterns
# see: https://flask.palletsprojects.com/en/1.1.x/errorhandling/
# see: https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/

# flask-expects-json is being used to validate incoming json
# see: https://github.com/Fischerfredl/flask-expects-json


def register_error_handlers(app):
    """
    This is a simple helper function to be used during app initialization to attach the
    error handlers found below.
    """
    app.register_error_handler(BadRequest, handle_bad_request)
    app.register_error_handler(HTTPException, handle_generic_exception)


def handle_bad_request(error):
    """
    Used to expose error messages provided by flask-expects-json.  This function is
    called when any BadRequest exception is thrown in the app.
    """
    return {
        "error": error.name,
        "status_code": error.code,
        # flask-expects-json puts the validation error in the error
        # description field so we'll access the message from there
        # See: https://github.com/Fischerfredl/flask-expects-json#error-handling
        "message": error.description.message,
    }, error.code


def handle_generic_exception(error):
    """
    Used to provide a consistent error format.  This function is called when any
    HTTPException exception is thrown in the app.
    """
    return {
        "error": error.name,
        "status_code": error.code,
        "message": error.description,
    }, error.code
