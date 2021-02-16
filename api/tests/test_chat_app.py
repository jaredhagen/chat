import json


def test_get_rooms(integration_client):
    response = integration_client.get(
        '/rooms', headers={'Authorization': 'Bearer test'})
    assert {
        "error": "Unauthorized",
        "message": "Bearer authentication required.  Bearer <username>",
        "status_code": 401
    } == response.get_json()
