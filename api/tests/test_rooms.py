# Used to remove id attributes from the room objects returned by the
# api. The room ids are randomly generated so I'm removing them to
# simplify testing. In a real world scenario I'd likely spend the time
# to figure out how to configure the app to generate predictable or
# constant ids during tests.  Done simply for the sake of time.
def remove_id(dict):
    del dict['id']
    return dict


def test_unauthorized_add_room(integration_client, unauthorized_user):
    response = integration_client.post(
        '/rooms', json={'name': 'Room 237'}, headers=unauthorized_user)
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Bearer authentication required.  Bearer <username>',
        'status_code': 401
    }


def test_add_room(integration_client, authorized_user):
    response = integration_client.post(
        '/rooms', json={'name': 'Room 237'}, headers=authorized_user)
    room = response.get_json()
    room_sans_id = remove_id(room)
    assert room_sans_id == {
        'name': 'Room 237',
        'creator': 'gandalf'
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
        '/rooms', json={'name': 'Room 104'}, headers=authorized_user)
    integration_client.post(
        '/rooms', json={'name': 'Room 237'}, headers=authorized_user)
    response = integration_client.get('/rooms', headers=authorized_user)

    rooms = response.get_json()['rooms']
    rooms_sans_ids = [remove_id(room) for room in rooms]
    assert rooms_sans_ids == [
        {
            'name': 'Room 104',
            'creator': 'gandalf'
        },
        {
            'name': 'Room 237',
            'creator': 'gandalf'
        }
    ]
