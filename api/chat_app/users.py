"""
This module defines a flask Blueprint for registering and verifying users.
"""

from flask import Blueprint, request
from flask_expects_json import expects_json
from werkzeug.exceptions import Unauthorized

from chat_app.dynamodb import add_item, get_item, PK, SK, USER_PARTITION_KEY


bp = Blueprint("users", __name__, url_prefix="/users")


add_user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 100},
    },
    "required": ["username"],
    "additionalProperties": False,
}


@bp.route("", methods=["POST"])
@expects_json(add_user_schema)
def add_user():
    """
    Handles: POST /users

    Adds a user to the DynamoDB table.
    """
    username = request.json["username"]
    add_item({PK: USER_PARTITION_KEY, SK: username})
    return {"username": username}


user_login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 100},
    },
    "required": ["username"],
    "additionalProperties": False,
}


@bp.route("/login", methods=["POST"])
@expects_json(user_login_schema)
def user_login():
    """
    Handles: POST /users

    Looks up a user in the DynamoDB table. Returns a 401 if the user doesn't exist
    otherwise returns the username.
    """
    username = request.json["username"]
    item = get_item({PK: USER_PARTITION_KEY, SK: username})
    if item is None:
        raise Unauthorized("Invalid credentials.")
    return {"username": username}
