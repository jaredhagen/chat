import ulid

from boto3.dynamodb.conditions import Key
from flask import Blueprint, request
from flask_expects_json import expects_json

from chat_app.auth import auth
from chat_app.dynamodb import get_chat_table, PK, ROOM_PARTITION_KEY, SK


ROOM_ID_PREFIX = "ROM"


def new_room_id():
    return "{}{}".format(ROOM_ID_PREFIX, str(ulid.new()))


def room_from_item(item):
    return {
        'id': item[SK],
        'name': item['name'],
        'creator': item['creator']
    }


bp = Blueprint('rooms', __name__, url_prefix='/rooms')

add_room_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
    },
    'required': ['name']
}


@bp.route('', methods=['POST'])
@expects_json(add_room_schema)
@auth.login_required
def add_room():
    username = auth.current_user()
    room_id = new_room_id()
    room_name = request.json['name']

    get_chat_table().put_item(
        Item={
            PK: ROOM_PARTITION_KEY,
            SK: room_id,
            'name': room_name,
            'creator': username
        }
    )
    return {
        'id': room_id,
        'name': room_name,
        'creator': username
    }


@bp.route('', methods=['GET'])
@auth.login_required
def get_rooms():
    response = get_chat_table().query(
        KeyConditionExpression=Key(
            PK).eq(ROOM_PARTITION_KEY)
    )
    items = response['Items']
    return {
        'rooms': [room_from_item(item) for item in items]
    }
