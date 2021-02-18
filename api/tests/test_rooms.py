import time

# Used to remove generated attributes from the message objects returned
# by the api. I'm removing them to simplify testing. In a real world 
# scenario I'd likely spend the time to figure out how to configure the
# app to generate predictable or constant attributes during tests. 
# Custom assertions would also be a possible solution. Done simply for
# the sake of time.
def remove_generated_values(dict):
    del dict['lastActiveAt']
    return dict


def test_unauthorized_add_room(integration_client, unauthorized_user):
    response = integration_client.post(
        '/rooms', json={'id': 'Room 237'}, headers=unauthorized_user)
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Bearer authentication required.  Bearer <username>',
        'status_code': 401
    }


def test_add_room(integration_client, authorized_user):
    response = integration_client.post(
        '/rooms', json={'id': 'Room 237'}, headers=authorized_user)
    room = response.get_json()
    assert remove_generated_values(room) == {
        'id': 'Room 237',
        'name': 'Room 237'
    }


def test_unauthorized_list_rooms(integration_client, unauthorized_user):
    response = integration_client.get('/rooms', headers=unauthorized_user)
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Bearer authentication required.  Bearer <username>',
        'status_code': 401
    }


def test_empty_list_rooms(integration_client, authorized_user):
    response = integration_client.get('/rooms', headers=authorized_user)
    assert response.get_json() == {"rooms": []}


def test_list_rooms(integration_client, authorized_user):
    integration_client.post(
        '/rooms', json={'id': 'Room 104'}, headers=authorized_user)
    integration_client.post(
        '/rooms', json={'id': 'Room 237'}, headers=authorized_user)
    response = integration_client.get('/rooms', headers=authorized_user)
    rooms = response.get_json()['rooms']
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {
            'id': 'Room 104',
            'name': 'Room 104'
        },
        {
            'id': 'Room 237',
            'name': 'Room 237'
        }
    ]


def test_list_rooms_by_activity(integration_client, authorized_user):
    integration_client.post(
        '/rooms', json={'id': 'Room 104'}, headers=authorized_user)
    integration_client.post(
        '/rooms', json={'id': 'Room 237'}, headers=authorized_user)
    response = integration_client.get('/rooms', headers=authorized_user)
    rooms = response.get_json()['rooms']
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {
            'id': 'Room 104',
            'name': 'Room 104'
        },
        {
            'id': 'Room 237',
            'name': 'Room 237'
        }
    ]
    time.sleep(1)
    integration_client.post(
        '/rooms/{}/messages'.format('Room 237'), json={'content': 'Hola'}, headers=authorized_user)
    response = integration_client.get('/rooms', headers=authorized_user)
    rooms = response.get_json()['rooms']
    rooms_sans_generated = [remove_generated_values(room) for room in rooms]
    assert rooms_sans_generated == [
        {
            'id': 'Room 237',
            'name': 'Room 237'
        },
        {
            'id': 'Room 104',
            'name': 'Room 104'
        }
    ]
