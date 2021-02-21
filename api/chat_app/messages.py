"""
This module defines a flask Blueprint for adding and listing Messages.
"""
from dataclasses import dataclass, field

import ulid

from flask import Blueprint, request
from flask_expects_json import expects_json
from werkzeug.exceptions import NotFound

from chat_app.auth import auth
from chat_app.rooms import Room
from chat_app.dynamodb import (
    add_item,
    epoch_time,
    get_item,
    PK,
    query_partition,
    ROOM_PARTITION_KEY,
    SK,
    update_item,
)


def new_message_id():
    """
    Returns a string representation of a ULID.  Used when creating a new Message.
    """
    return str(ulid.new())


@dataclass
class Message:
    """
    A simple dataclass to represent a Message
    """

    author: str
    content: str
    id: int = field(default_factory=new_message_id)  # pylint: disable=C0103
    created_at: int = field(default_factory=epoch_time)

    def to_dynamodb_item(self, room_id):
        """
        Used to get a dict representation of a Message for storage in DynamoDB
        """
        return {
            PK: room_id,
            SK: self.id,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at,
        }

    def to_api_response(self):
        """
        Used to get a dict representation of a Message for an API response
        """
        return {
            "author": self.author,
            "content": self.content,
            "createdAt": self.created_at,
            "id": self.id,
        }

    @staticmethod
    def from_dynamodb_item(item):
        """
        Used to create a Message from a dict representing a DynamoDB item
        """
        return Message(
            item["author"], item["content"], item[SK], int(item["created_at"])
        )


bp = Blueprint("messages", __name__, url_prefix="/rooms/<room_id>/messages")

add_message_schema = {
    "type": "object",
    "properties": {
        "content": {"type": "string", "minLength": 1, "maxLength": 1000},
    },
    "required": ["content"],
    "additionalProperties": False,
}


@bp.route("", methods=["POST"])
@auth.login_required
@expects_json(add_message_schema)
def add_message(room_id):
    """
    Handles: POST /rooms/<room_id>/messages

    This function looks up the room provided via the url param to ensure the room
    exists.  It then creates a message and updates the last_active_at attribute of the
    room and write both the updated room and message to Dynamo
    """
    room_item = get_item({PK: ROOM_PARTITION_KEY, SK: room_id})
    if room_item is None:
        raise NotFound("Can't add message to non-existent room")

    message = Message(auth.current_user(), request.json["content"])

    room = Room.from_dynamodb_item(room_item)
    room.last_active_at = message.created_at

    add_item(message.to_dynamodb_item(room_id))
    update_item(room.to_dynamodb_item())

    return message.to_api_response()


@bp.route("", methods=["GET"])
@auth.login_required
def get_messages(room_id):
    """
    Handles: GET /rooms/<room_id>/messages

    Simply retrieves and returns 50 latest messages in the given room.
    """
    items = query_partition(room_id, limit=50, scan_index_forward=False)
    return {
        "messages": [
            Message.from_dynamodb_item(item).to_api_response() for item in items
        ]
    }
