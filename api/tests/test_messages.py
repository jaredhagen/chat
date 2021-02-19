import time

import pytest


# Used to remove generated attributes from the message objects returned
# by the api. I'm removing them to simplify testing. In a real world
# scenario I'd likely spend the time to figure out how to configure the
# app to generate predictable or constant attributes during tests.
# Custom assertions would also be a possible solution. Done simply for
# the sake of time.
def remove_generated_values(dict):
    del dict["id"]
    del dict["created_at"]
    return dict


@pytest.fixture
def with_room(integration_client, authorized_user):
    response = integration_client.post(
        "/rooms", json={"id": "Room 104"}, headers=authorized_user
    )
    return response.get_json()["id"]


def test_unauthorized_add_message(integration_client, unauthorized_user, with_room):
    response = integration_client.post(
        "/rooms/{}/messages".format(with_room),
        json={"content": "Hello"},
        headers=unauthorized_user,
    )
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_add_message(integration_client, authorized_user, with_room):
    response = integration_client.post(
        "/rooms/{}/messages".format(with_room),
        json={"content": "Bonjour"},
        headers=authorized_user,
    )
    message = response.get_json()
    assert remove_generated_values(message) == {
        "author": "gandalf",
        "content": "Bonjour",
    }


def test_add_message_to_non_existent_room(integration_client, authorized_user):
    response = integration_client.post(
        "/rooms/{}/messages".format("make believe"),
        json={"content": "Bonjour"},
        headers=authorized_user,
    )
    assert response.get_json() == {
        "error": "Not Found",
        "message": "Can't add message to non-existent room",
        "status_code": 404,
    }


def test_unauthorized_list_messages(integration_client, unauthorized_user, with_room):
    response = integration_client.get(
        "/rooms/{}/messages".format(with_room), headers=unauthorized_user
    )
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401,
    }


def test_empty_list_messages(integration_client, authorized_user, with_room):
    response = integration_client.get(
        "/rooms/{}/messages".format(with_room), headers=authorized_user
    )
    assert response.get_json() == {"messages": []}


def test_list_messages(integration_client, authorized_user, with_room):
    integration_client.post(
        "/rooms/{}/messages".format(with_room),
        json={"content": "Hola"},
        headers=authorized_user,
    )
    integration_client.post(
        "/rooms/{}/messages".format(with_room),
        json={"content": "Guten Tag"},
        headers=authorized_user,
    )
    response = integration_client.get(
        "/rooms/{}/messages".format(with_room), headers=authorized_user
    )

    messages = response.get_json()["messages"]
    messages_sans_generated = [remove_generated_values(message) for message in messages]
    assert messages_sans_generated == [
        {"author": "gandalf", "content": "Hola"},
        {"author": "gandalf", "content": "Guten Tag"},
    ]


def test_message_activity_updates_room_activity(
    integration_client, authorized_user, with_room
):
    rooms_before = integration_client.get("/rooms", headers=authorized_user).get_json()
    time.sleep(1)
    integration_client.post(
        "/rooms/{}/messages".format(with_room),
        json={"content": "Hola"},
        headers=authorized_user,
    )
    rooms_after = integration_client.get("/rooms", headers=authorized_user).get_json()
    assert (
        rooms_before["rooms"][0]["lastActiveAt"]
        < rooms_after["rooms"][0]["lastActiveAt"]
    )
