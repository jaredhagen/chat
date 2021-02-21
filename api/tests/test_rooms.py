# Used to remove generated attributes from the message objects returned
# by the api. I'm removing them to simplify testing. In a real world
# scenario I'd likely spend the time to figure out how to configure the
# app to generate predictable or constant attributes during tests.
# Custom assertions would also be a possible solution. Done simply for
# the sake of time.
def remove_generated_values(dict):
    del dict["lastActiveAt"]
    return dict


def test_unauthorized_add_room(add_room, unauthorized_header):
    response = add_room("Room 237", headers=unauthorized_header)
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_add_room(add_room):
    response = add_room("Room 237")
    room = response.get_json()
    assert remove_generated_values(room) == {"id": "Room 237", "name": "Room 237"}


def test_add_existing_room(add_room):
    add_room("Room 237")
    response = add_room("Room 237")
    assert response.get_json() == {
        "error": "Conflict",
        "message": "Resource already exists.",
        "status_code": 409,
    }


def test_add_room_empty_string(add_room):
    response = add_room("")
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'' is too short",
        "status_code": 400,
    }


def test_add_room_long_string(add_room):
    long_name = "x" * 101
    response = add_room(long_name)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'{}' is too long".format(long_name),
        "status_code": 400,
    }


def test_add_room_non_string(add_room):
    non_string = 0
    response = add_room(non_string)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "{} is not of type 'string'".format(non_string),
        "status_code": 400,
    }


def test_add_room_additional_attributes(add_room):
    response = add_room(None, json={"id": "Room 237", "extra": True})
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "Additional properties are not allowed ('extra' was unexpected)",
        "status_code": 400,
    }


def test_unauthorized_list_rooms(list_rooms, unauthorized_header):
    response = list_rooms(headers=unauthorized_header)
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_empty_list_rooms(list_rooms):
    response = list_rooms()
    assert response.get_json() == {"rooms": []}


def test_list_rooms(add_room, list_rooms):
    add_room("Room 104")
    add_room("Room 237")
    response = list_rooms()
    rooms = response.get_json()["rooms"]
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {"id": "Room 237", "name": "Room 237"},
        {"id": "Room 104", "name": "Room 104"},
    ]


def test_list_rooms_by_activity(add_room, list_rooms, add_message):
    add_room("Room 104")
    add_room("Room 237")
    response = list_rooms()
    rooms = response.get_json()["rooms"]
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {"id": "Room 237", "name": "Room 237"},
        {"id": "Room 104", "name": "Room 104"},
    ]
    add_message("Room 104", "Hello")
    response = list_rooms()
    rooms = response.get_json()["rooms"]
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {"id": "Room 104", "name": "Room 104"},
        {"id": "Room 237", "name": "Room 237"},
    ]
