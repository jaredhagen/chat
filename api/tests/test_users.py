import pytest


@pytest.fixture
def login_user(integration_client):
    def post_user_login(username, headers=None, json=None):
        return integration_client.post(
            "/users/login", json=json if json is not None else {"username": username}
        )

    return post_user_login


def test_register_user(register_user):
    response = register_user("gandalf")
    assert response.get_json() == {"username": "gandalf"}


def test_register_user_empty_string(register_user):
    response = register_user("")
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'' is too short",
        "status_code": 400,
    }


def test_register_user_long_string(register_user):
    long_content = "x" * 101
    response = register_user(long_content)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'{}' is too long".format(long_content),
        "status_code": 400,
    }


def test_register_user_non_string(register_user):
    non_string = 0
    response = register_user(non_string)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "{} is not of type 'string'".format(non_string),
        "status_code": 400,
    }


def test_register_user_additional_attributes(register_user):
    response = register_user(None, json={"username": "gandalf", "extra": True})
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "Additional properties are not allowed ('extra' was unexpected)",
        "status_code": 400,
    }


def test_user_login(register_user, login_user):
    # register user so the login works
    register_user("gandalf")
    response = login_user("gandalf")
    assert response.get_json() == {"username": "gandalf"}


def test_user_login_unauthorized(login_user):
    response = login_user("gandalf")
    assert response.get_json() == {
        "error": "Unauthorized",
        "message": "Invalid credentials.",
        "status_code": 401,
    }


def test_user_login_empty_string(login_user):
    response = login_user("")
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'' is too short",
        "status_code": 400,
    }


def test_user_login_long_string(login_user):
    long_content = "x" * 101
    response = login_user(long_content)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "'{}' is too long".format(long_content),
        "status_code": 400,
    }


def test_user_login_non_string(login_user):
    non_string = 0
    response = login_user(non_string)
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "{} is not of type 'string'".format(non_string),
        "status_code": 400,
    }


def test_user_login_additional_attributes(login_user):
    response = login_user(None, json={"username": "gandalf", "extra": True})
    assert response.get_json() == {
        "error": "Bad Request",
        "message": "Additional properties are not allowed ('extra' was unexpected)",
        "status_code": 400,
    }
