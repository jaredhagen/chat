from flask import jsonify, make_response
from werkzeug.exceptions import BadRequest, Forbidden, HTTPException, Unauthorized

# for more information on flask error handling patterns
# see: https://flask.palletsprojects.com/en/1.1.x/errorhandling/
# see: https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/

# flask-expects-json is being used to validate incoming json
# see: https://github.com/Fischerfredl/flask-expects-json


def register_error_handlers(app):
    app.register_error_handler(BadRequest, handle_bad_request)
    app.register_error_handler(HTTPException, handle_generic_exception)


def handle_bad_request(error):
    return {
        'error': error.name,
        'status_code': error.code,
        # flask-expects-json puts the validation error in the error
        # description field so we'll access the message from there
        # See: https://github.com/Fischerfredl/flask-expects-json#error-handling
        'message': error.description.message
    }, error.code


def handle_generic_exception(error):
    return {
        'error': error.name,
        'status_code': error.code,
        'message': error.description
    }, error.code
