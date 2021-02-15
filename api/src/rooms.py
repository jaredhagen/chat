import ulid

from boto3.dynamodb.conditions import Key
from flask import Blueprint, request
from flask_expects_json import expects_json

from src.auth import auth
from src.dynamodb import get_chat_table, PK, ROOM_PARTITION_KEY, SK


ROOM_ID_PREFIX = "ROM"


def new_room_id():
    return "{}{}".format(ROOM_ID_PREFIX, str(ulid.new()))


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
    room_id = new_room_id()
    room_name = request.json['name']

    response = get_chat_table().put_item(
        Item={
            PK: ROOM_PARTITION_KEY,
            SK: room_id,
            'name': room_name
        }
    )
    return {
        'id': room_id,
        'name': room_name
    }


@bp.route('', methods=['GET'])
@auth.login_required
def get_rooms():
    response = get_chat_table().query(
        KeyConditionExpression=Key(
            PK).eq(ROOM_PARTITION_KEY)
    )
    return {
        'rooms': response['Items']
    }
