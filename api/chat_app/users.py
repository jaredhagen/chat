from botocore.exceptions import ClientError
from flask import Blueprint, current_app, request
from flask_expects_json import expects_json
from werkzeug.exceptions import Conflict, InternalServerError, Unauthorized

from chat_app.auth import auth
from chat_app.dynamodb import get_chat_table, PK, SK, USER_PARTITION_KEY

bp = Blueprint('users', __name__, url_prefix="/users")

add_user_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
    },
    'required': ['username']
}


@bp.route('', methods=['POST'])
@expects_json(add_user_schema)
def add_user():
    username = request.json['username']
    try:
        get_chat_table().put_item(
            Item={
                PK: USER_PARTITION_KEY,
                SK: username
            },
            ConditionExpression=('attribute_not_exists({})'.format(PK))
        )
    except ClientError as e:
        current_app.logger.error(e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise Conflict('Username already exists.')
        else:
            raise e
    else:
        return {
            'username': username
        }


user_login_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
    },
    'required': ['username']
}


@bp.route('/login', methods=['POST'])
@expects_json(user_login_schema)
def user_login():
    username = request.json['username']
    try:
        response = get_chat_table().get_item(
            Key={
                PK: USER_PARTITION_KEY,
                SK: username
            }
        )
    except ClientError as e:
        current_app.logger.error(e)
        raise InternalServerError()
    else:
        current_app.logger.debug(response)
        if 'Item' in response:
            token = response['Item'][SK]
            return {'token': token}
        else:
            raise Unauthorized("Invalid credentials.")
