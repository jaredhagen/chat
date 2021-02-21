"""
This module contains functions for verifying https Authorization headers for use with
flask_http auth.
"""
from botocore.exceptions import ClientError
from flask import current_app
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Forbidden, InternalServerError, Unauthorized

from chat_app.dynamodb import get_chat_table, PK, SK, USER_PARTITION_KEY

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    """
    Used to verify the authrozation header included on requests. This function is run
    when a route is decorated with the @auth.login_required decorator.

    The token which is currently just the user's username is checked against the
    existing users in the dynamo table.  If the user exists they are authorized.
    Otherwise we return None and the flask_httpauth package turns that into a 401.
    """
    if not token:
        return None
    try:
        response = get_chat_table().get_item(Key={PK: USER_PARTITION_KEY, SK: token})
    except ClientError as error:
        current_app.logger.error(error)
        return None
    else:
        if "Item" in response:
            username = response["Item"][SK]
            return username
        return None


@auth.error_handler
def auth_error(status):
    """
    The Flask_HTTPAuth package doesn't raise http exceptions like it should. Instead it
    requires you to implement an error handler function that accepts a 401 or 403
    status. Here I'm raising excpetions so that our error handlers in the errors package
     will get triggered.

    See: https://flask-httpauth.readthedocs.io/en/latest/#flask_httpauth.HTTPBasicAuth.error_handler

    Note: I have no idea how efficient this is. In a real world scenario I'd put time
    into figuring that out. Alternative solutions include importing the error handlers
    and calling them here or using a different library or no library at all.
    """
    if status == 401:
        raise Unauthorized("Bearer authentication required.  Bearer <username>")
    if status == 403:
        raise Forbidden()
    raise InternalServerError()
