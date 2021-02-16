import pytest


# Used to remove id attributes from the message objects returned by the
# api. The messages ids are randomly generated so I'm removing them to
# simplify testing. In a real world scenario I'd likely spend the time
# to figure out how to configure the app to generate predictable or
# constant ids during tests.  Done simply for the sake of time.
def remove_id(dict):
    del dict['id']
    return dict


@pytest.fixture
def with_room(integration_client, authorized_user):
    response = integration_client.post(
        '/rooms', json={'name': 'Room 104'}, headers=authorized_user)
    return response.get_json()['id']


def test_unauthorized_add_message(integration_client, unauthorized_user, with_room):
    response = integration_client.post(
        '/rooms/{}/messages'.format(with_room), json={'content': 'Hello'}, headers=unauthorized_user)
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Bearer authentication required.  Bearer <username>',
        'status_code': 401
    }


def test_add_message(integration_client, authorized_user, with_room):
    response = integration_client.post(
        '/rooms/{}/messages'.format(with_room), json={'content': 'Bonjour'}, headers=authorized_user)
    message = response.get_json()
    message_sans_id = remove_id(message)
    assert message_sans_id == {
        'content': 'Bonjour',
        'author': 'gandalf'
    }


def test_unauthorized_list_messages(integration_client, unauthorized_user, with_room):
    response = integration_client.get(
        '/rooms/{}/messages'.format(with_room), headers=unauthorized_user)
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Bearer authentication required.  Bearer <username>',
        'status_code': 401
    }


def test_empty_list_messages(integration_client, authorized_user, with_room):
    response = integration_client.get(
        '/rooms/{}/messages'.format(with_room), headers=authorized_user)
    assert response.get_json() == {"messages": []}


def test_list_messages(integration_client, authorized_user, with_room):
    integration_client.post(
        '/rooms/{}/messages'.format(with_room), json={'content': 'Hola'}, headers=authorized_user)
    integration_client.post(
        '/rooms/{}/messages'.format(with_room), json={'content': 'Guten Tag'}, headers=authorized_user)
    response = integration_client.get(
        '/rooms/{}/messages'.format(with_room), headers=authorized_user)

    messages = response.get_json()['messages']
    messages_sans_ids = [remove_id(message) for message in messages]
    assert messages_sans_ids == [
        {
            'content': 'Hola',
            'author': 'gandalf'
        },
        {
            'content': 'Guten Tag',
            'author': 'gandalf'
        }
    ]
