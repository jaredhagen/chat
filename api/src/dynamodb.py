import boto3
import os

from flask import g

# If you're unfamiliar with DynamoDB I highly recommend watching the
# following video. It's long but worth the time IMHO.
# See: https://www.youtube.com/watch?v=HaEPXoXVf2k

CHAT_DYNAMODB_LOCALHOST_PORT = os.getenv('CHAT_DYNAMODB_LOCALHOST_PORT')
CHAT_DYNAMODB_TABLE_NAME = os.getenv('CHAT_DYNAMODB_TABLE_NAME')

# I'm making using of DynamoDB index overloading so these are generic
# key attribute names.
# See: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html
PK = 'pk'
SK = 'sk'

# I'm using a constant value for the users and rooms partition keys
# since this dynamodb table is currently single tenent. If the table was
# multitenent I would use an account id or something along those lines
# to partition the users and rooms by account.
USER_PARTITION_KEY = 'users'
ROOM_PARTITION_KEY = 'rooms'


def get_chat_table():
    if 'chat_table' not in g:
        dynamodb = get_dynamodb()
        g.chat_table = dynamodb.Table(CHAT_DYNAMODB_TABLE_NAME)

    return g.chat_table


def get_dynamodb():
    if 'dynamodb' not in g:
        g.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://dynamodb:{}".format(
                CHAT_DYNAMODB_LOCALHOST_PORT
            ),
            region_name="us-east-1"
        )

    return g.dynamodb


def add_room():
    response = get_chat_table().put_item(
        Item={
            PK: ROOM_PARTITION_KEY,
            SK: room_id,
            'name': room_name
        }
    )
