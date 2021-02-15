import boto3
import os

from flask import current_app, g

# If you're unfamiliar with DynamoDB I highly recommend watching the
# following video. It's long but worth the time IMHO.
# See: https://www.youtube.com/watch?v=HaEPXoXVf2k

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
        table_name = current_app.config['CHAT_DYNAMODB_TABLE_NAME']
        dynamodb = get_dynamodb()
        g.chat_table = dynamodb.Table(table_name)

    return g.chat_table


def get_dynamodb():
    if 'dynamodb' not in g:
        port = current_app.config['CHAT_DYNAMODB_LOCALHOST_PORT']
        g.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://dynamodb:{}".format(port),
            region_name="us-east-1"
        )

    return g.dynamodb
