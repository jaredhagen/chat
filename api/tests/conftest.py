import boto3
import pytest
import ulid

from chat_app import create_app

TESTS_DYNAMODB_ENDPOINT = "http://tests-dynamodb:8000"

dynamodb = boto3.client(
    "dynamodb", endpoint_url=TESTS_DYNAMODB_ENDPOINT, region_name="us-east-1"
)


@pytest.fixture
def integration_client():
    # We want to start with a fresh DynamoDB table for every one of our tests so we'll
    # generate a random table name create the table and then inject that into our
    # application config.  One the test is finished running remove the table.
    table_name = str(ulid.new())
    create_table(table_name)
    app = create_app(
        {
            "TESTING": True,
            "CHAT_DYNAMODB_ENDPOINT_URL": TESTS_DYNAMODB_ENDPOINT,
            "CHAT_DYNAMODB_TABLE_NAME": table_name,
        }
    )
    yield app.test_client()
    delete_table(table_name)


@pytest.fixture
def register_user(integration_client):
    def post_user(username, json=None):
        return integration_client.post(
            "/users", json=json if json is not None else {"username": username}
        )

    return post_user


@pytest.fixture
def authorized_header(register_user):
    register_user("gandalf")
    return {"Authorization": "Bearer gandalf"}


@pytest.fixture
def unauthorized_header():
    return {"Authorization": "Bearer hackerman"}


@pytest.fixture
def add_room(integration_client, authorized_header):
    def post_room(room_id, headers=None, json=None):
        return integration_client.post(
            "/rooms",
            json=json if json is not None else {"id": room_id},
            headers=headers if headers is not None else authorized_header,
        )

    return post_room


@pytest.fixture
def list_rooms(integration_client, authorized_header):
    def get_rooms(headers=None):
        return integration_client.get(
            "/rooms",
            headers=headers if headers is not None else authorized_header,
        )

    return get_rooms


@pytest.fixture
def add_message(integration_client, authorized_header):
    def post_message(room_id, message_content, headers=None, json=None):
        return integration_client.post(
            "/rooms/{}/messages".format(room_id),
            json=json if json is not None else {"content": message_content},
            headers=headers if headers is not None else authorized_header,
        )

    return post_message


def create_table(table_name):
    return dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )


def delete_table(table_name):
    return dynamodb.delete_table(TableName=table_name)
