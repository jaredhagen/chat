import ulid

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from flask import Blueprint, request
from flask_expects_json import expects_json
from werkzeug.exceptions import InternalServerError

from chat_app.auth import auth
from chat_app.dynamodb import get_chat_table, PK, SK

MESSAGE_ID_PREFIX = "MSG"


def new_message_id():
    return "{}{}".format(MESSAGE_ID_PREFIX, str(ulid.new()))


def message_from_item(item):
    return {
        'id': item[SK],
        'content': item['content'],
        'author': item['author']
    }


bp = Blueprint('messages', __name__, url_prefix='/rooms/<room_id>/messages')

add_message_schema = {
    'type': 'object',
    'properties': {
        'content': {'type': 'string'},
    },
    'required': ['content']
}


@bp.route('', methods=['POST'])
@expects_json(add_message_schema)
@auth.login_required
def add_message(room_id):
    username = auth.current_user()
    message_id = new_message_id()
    message_content = request.json['content']

    try:
        get_chat_table().put_item(
            Item={
                PK: room_id,
                SK: message_id,
                'content': message_content,
                'author': username
            }
        )
    except ClientError as e:
        raise InternalServerError()
    else:
        return {
            'id': message_id,
            'content': message_content,
            'author': username
        }


@bp.route('', methods=['GET'])
@auth.login_required
def get_messages(room_id):
    try:
        response = get_chat_table().query(
            KeyConditionExpression=Key(PK).eq(room_id)
        )
    except ClientError as e:
        raise
    else:
        items = response['Items']
        return {
            'messages': [message_from_item(item) for item in items]
        }
