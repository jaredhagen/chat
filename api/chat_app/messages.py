import ulid

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from dataclasses import dataclass, field
from flask import Blueprint, request
from flask_expects_json import expects_json
from werkzeug.exceptions import InternalServerError, NotFound

from chat_app.auth import auth
from chat_app.rooms import Room
from chat_app.dynamodb import epoch_time, get_item, query_partition, add_item, update_item, PK, SK, ROOM_PARTITION_KEY


def new_message_id():
    return str(ulid.new())


@dataclass
class Message:
    author: str
    content: str
    id: int = field(default_factory=new_message_id)
    created_at: int = field(default_factory=epoch_time)

    def to_dynamodb_item(self, room_id):
        return {
            PK: room_id,
            SK: self.id,
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at
        }

    def to_api_response(self):
        return {
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at,
            'id': self.id
        }

    @staticmethod
    def from_dynamodb_item(item):
        return Message(
            item['author'],
            item['content'],
            item[SK],
            int(item['created_at'])
        )


bp = Blueprint('messages', __name__, url_prefix='/rooms/<room_id>/messages')

add_message_schema = {
    'type': 'object',
    'properties': {
        'content': {'type': 'string'},
    },
    'required': ['content']
}


@bp.route('', methods=['POST'])
@auth.login_required
@expects_json(add_message_schema)
def add_message(room_id):
    room_item = get_item({ PK: ROOM_PARTITION_KEY, SK: room_id })
    if room_item is None:
        raise NotFound("Can't add message to non-existent room")
    room = Room.from_dynamodb_item(room_item)
    message = Message(auth.current_user(), request.json['content'])
    room.last_active_at = message.created_at
    add_item(message.to_dynamodb_item(room_id))
    update_item(room.to_dynamodb_item())
    return message.to_api_response()


@bp.route('', methods=['GET'])
@auth.login_required
def get_messages(room_id):
    items = query_partition(room_id)
    return {
        'messages': [Message.from_dynamodb_item(item).to_api_response() for item in items]
    }
