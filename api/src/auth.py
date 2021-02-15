
from botocore.exceptions import ClientError
from flask import abort, current_app
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Forbidden, InternalServerError, Unauthorized

from src.dynamodb import get_chat_table, PK, SK, USER_PARTITION_KEY

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        response = get_chat_table().get_item(
            Key={
                PK: USER_PARTITION_KEY,
                SK: token
            }
        )
    except ClientError as e:
        return False
    else:
        if 'Item' in response:
            username = response['Item'][SK]
            return username
        return False


# The Flask_HTTPAuth package doesn't raise http exceptions like it
# should. Instead it requires you to implement an error handler function
# that accepts a 401 or 403 status. Here I'm raising excpetions so that
# our error handlers in the errors package will get triggered.
#
# See: https://flask-httpauth.readthedocs.io/en/latest/#flask_httpauth.HTTPBasicAuth.error_handler
#
# I have no idea how efficient this is. In a real world scenario I'd put
# time into figuring that out. Alternative solutions include importing
# the error handlers and calling them here or using a different library
# or no library at all.
@auth.error_handler
def auth_error(status):
    if status == 401:
        raise Unauthorized(
            'Bearer authentication required.  Bearer <username>')
    elif status == 403:
        raise Forbidden()
