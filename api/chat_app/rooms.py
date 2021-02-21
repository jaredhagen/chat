"""
This module defines a flask Blueprint for adding and listing Rooms.
"""

from dataclasses import dataclass, field
from flask import Blueprint, request
from flask_expects_json import expects_json

from chat_app.auth import auth
from chat_app.dynamodb import (
    add_item,
    epoch_time,
    PK,
    query_partition,
    ROOM_PARTITION_KEY,
    SK,
)


@dataclass
class Room:
    """
    A simple dataclass to represent a Room
    """

    id: str  # pylint: disable=C0103
    last_active_at: int = field(default_factory=epoch_time)

    def to_dynamodb_item(self):
        """
        Used to get a dict representation of a Room for storage in DynamoDB
        """
        return {
            PK: ROOM_PARTITION_KEY,
            SK: self.id,
            "last_active_at": self.last_active_at,
        }

    def to_api_response(self):
        """
        Used to get a dict representation of a Room for an API response
        """
        return {"id": self.id, "lastActiveAt": self.last_active_at, "name": self.id}

    @staticmethod
    def from_dynamodb_item(item: dict):
        """
        Used to create a Room from a dict representing a DynamoDB item
        """
        return Room(
            item[SK],
            int(item["last_active_at"]),
        )


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


add_room_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 1, "maxLength": 100},
    },
    "required": ["id"],
    "additionalProperties": False,
}


@bp.route("", methods=["POST"])
@auth.login_required
@expects_json(add_room_schema)
def add_room():
    """
    Handles: GET /rooms

    Simply adds a rooms to the DynamoDB table.
    """
    room = Room(request.json["id"])
    add_item(room.to_dynamodb_item())
    return room.to_api_response()


@bp.route("", methods=["GET"])
@auth.login_required
def get_rooms():
    """
    Handles: GET /rooms

    Simply retrieves and returns all the rooms.
    """
    items = query_partition(ROOM_PARTITION_KEY)
    rooms = [Room.from_dynamodb_item(item) for item in items]
    rooms.sort(key=(lambda room: room.last_active_at), reverse=True)
    return {"rooms": [room.to_api_response() for room in rooms]}
