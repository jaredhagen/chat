import boto3
import os
import pytest
import ulid

from chat_app import create_app

TESTS_DYNAMODB_ENDPOINT = "http://tests-dynamodb:8000"

dynamodb = boto3.client(
    "dynamodb", endpoint_url=TESTS_DYNAMODB_ENDPOINT, region_name="us-east-1"
)


@pytest.fixture
def integration_client():
    table_name = str(ulid.new())
    createTable(table_name)
    app = create_app(
        {
            "TESTING": True,
            "CHAT_DYNAMODB_ENDPOINT_URL": TESTS_DYNAMODB_ENDPOINT,
            "CHAT_DYNAMODB_TABLE_NAME": table_name,
        }
    )
    yield app.test_client()
    deleteTable(table_name)


@pytest.fixture
def authorized_user(integration_client):
    integration_client.post("/users", json={"username": "gandalf"})
    return {"Authorization": "Bearer gandalf"}


@pytest.fixture
def unauthorized_user():
    return {"Authorization": "Bearer hackerman"}


def createTable(table_name):
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


def deleteTable(table_name):
    return dynamodb.delete_table(TableName=table_name)
