import time

from dataclasses import dataclass, field
from flask import Blueprint, request
from flask_expects_json import expects_json

from chat_app.auth import auth
from chat_app.dynamodb import (
    epoch_time,
    query_partition,
    add_item,
    PK,
    ROOM_PARTITION_KEY,
    SK,
)


@dataclass
class Room:
    id: str
    last_active_at: int = field(default_factory=epoch_time)

    def to_dynamodb_item(self):
        return {
            PK: ROOM_PARTITION_KEY,
            SK: self.id,
            "last_active_at": self.last_active_at,
        }

    def to_api_response(self):
        return {"id": self.id, "lastActiveAt": self.last_active_at, "name": self.id}

    @staticmethod
    def from_dynamodb_item(item: dict):
        return Room(
            item[SK],
            int(item["last_active_at"]),
        )


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


add_room_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
    },
    "required": ["id"],
}


@bp.route("", methods=["POST"])
@auth.login_required
@expects_json(add_room_schema)
def add_room():
    room = Room(request.json["id"])
    add_item(room.to_dynamodb_item())
    return room.to_api_response()


@bp.route("", methods=["GET"])
@auth.login_required
def get_rooms():
    items = query_partition(ROOM_PARTITION_KEY)
    rooms = [Room.from_dynamodb_item(item) for item in items]
    rooms.sort(key=(lambda room: room.last_active_at), reverse=True)
    return {"rooms": [room.to_api_response() for room in rooms]}
