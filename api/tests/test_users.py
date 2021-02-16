def test_register_user(integration_client):
    response = integration_client.post(
        '/users', json={'username': 'gandalf'})
    assert response.get_json() == {"username": "gandalf"}


def gandalf_login(integration_client):
    # register user so the login works
    integration_client.post('/users', json={'username': 'gandalf'})
    response = integration_client.post(
        '/users/login', json={'username': 'gandalf'})
    assert response.get_json() == {"token": "gandalf"}


def test_unauthorized_user_login(integration_client):
    response = integration_client.post(
        '/users/login', json={'username': 'gandalf'})
    assert response.get_json() == {
        'error': 'Unauthorized',
        'message': 'Invalid credentials.',
        'status_code': 401
    }
