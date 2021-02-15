from botocore.exceptions import ClientError
from flask import Blueprint, request
from flask_expects_json import expects_json
from werkzeug.exceptions import Conflict

from src.dynamodb import get_chat_table, PK, SK, USER_PARTITION_KEY

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
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise Conflict('username already exists')
        else:
            raise e
    else:
        return {
            'username': username
        }
