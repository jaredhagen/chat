import pytest


# Used to remove generated attributes from the message objects returned
# by the api. I'm removing them to simplify testing. In a real world
# scenario I'd likely spend the time to figure out how to configure the
# app to generate predictable or constant attributes during tests.
# Custom assertions would also be a possible solution. Done simply for
# the sake of time.
def remove_generated_values(dict):
    del dict["id"]
    del dict["createdAt"]
    return dict


@pytest.fixture
def with_room(add_room):
    response = add_room("Room 104")
    return response.get_json()["id"]


@pytest.fixture
def list_messages(integration_client, authorized_header):
    def get_rooms(room_id, headers=None):
        return integration_client.get(
            "/rooms/{}/messages".format(room_id),
            headers=headers if headers is not None else authorized_header,
        )

    return get_rooms


def test_unauthorized_add_message(with_room, add_message, unauthorized_header):
    response = add_message(with_room, "Hello", headers=unauthorized_header)
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_add_message(with_room, add_message):
    response = add_message(
        with_room,
        "And he that breaks a thing to find out what it is has left the path of wisdom.",
    )
    message = response.get_json()
    assert remove_generated_values(message) == {
        "author": "gandalf",
        "content": "And he that breaks a thing to find out what it is has left the path of wisdom.",
    }


def test_add_message_to_non_existent_room(add_message):
    response = add_message("Make Believe", "Hello")
    assert response.get_json() == {
        "error": "Not Found",
        "message": "Can't add message to non-existent room",
        "status_code": 404,
    }


def test_add_message_empty_string(with_room, add_message):
    response = add_message(with_room, "")
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'' is too short",
        "status_code": 400,
    }


def test_add_message_long_string(with_room, add_message):
    long_content = "x" * 1001
    response = add_message(with_room, long_content)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'{}' is too long".format(long_content),
        "status_code": 400,
    }


def test_add_message_non_string(with_room, add_message):
    non_string = 0
    response = add_message(with_room, non_string)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "{} is not of type 'string'".format(non_string),
        "status_code": 400,
    }


def test_add_message_additional_attributes(with_room, add_message):
    response = add_message(with_room, None, json={"content": "Hello", "extra": True})
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "Additional properties are not allowed ('extra' was unexpected)",
        "status_code": 400,
    }


def test_unauthorized_list_messages(with_room, list_messages, unauthorized_header):
    response = list_messages(with_room, headers=unauthorized_header)
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_empty_list_messages(with_room, list_messages):
    response = list_messages(with_room)
    assert response.get_json() == {"messages": []}


def test_list_messages(with_room, add_message, list_messages):
    add_message(
        with_room,
        "It Is The Small Things, Everyday Deeds Of Ordinary Folk That Keeps The Darkness At Bay. Simple Acts Of Love And Kindness.",
    )
    add_message(
        with_room,
        "It is not despair, for despair is only for those who see the end beyond all doubt. We do not.",
    )
    response = list_messages(with_room)
    messages = response.get_json()["messages"]
    messages_sans_generated = [remove_generated_values(message) for message in messages]
    # Messages should be in reverse chronological order
    assert messages_sans_generated == [
        {
            "author": "gandalf",
            "content": "It is not despair, for despair is only for those who see the end beyond all doubt. We do not.",
        },
        {
            "author": "gandalf",
            "content": "It Is The Small Things, Everyday Deeds Of Ordinary Folk That Keeps The Darkness At Bay. Simple Acts Of Love And Kindness.",
        },
    ]


def test_list_50_messages(with_room, add_message, list_messages):
    for n in range(51):
        add_message(with_room, str(n))
    response = list_messages(with_room)
    messages = response.get_json()["messages"]
    assert len(messages) == 50


def test_new_messages_update_room_activity(with_room, list_rooms, add_message):
    rooms_before = list_rooms().get_json()["rooms"]
    add_message(with_room, "The wise speak only of what they know.")
    rooms_after = list_rooms().get_json()["rooms"]
    assert rooms_before[0]["lastActiveAt"] < rooms_after[0]["lastActiveAt"]
