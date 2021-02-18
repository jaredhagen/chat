import boto3
import os
import time

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import current_app, g
from werkzeug.exceptions import Conflict, InternalServerError, NotFound


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


def epoch_time():
    return int(time.time())


def get_chat_table():
    if 'chat_table' not in g:
        table_name = current_app.config['CHAT_DYNAMODB_TABLE_NAME']
        dynamodb = get_dynamodb()
        g.chat_table = dynamodb.Table(table_name)

    return g.chat_table


def get_dynamodb():
    if 'dynamodb' not in g:
        endpoint_url = current_app.config['CHAT_DYNAMODB_ENDPOINT_URL']
        g.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=endpoint_url,
            region_name="us-east-1"
        )

    return g.dynamodb


def add_item(item):
    try:
        get_chat_table().put_item(
            Item=item,
            ConditionExpression=('attribute_not_exists({})'.format(PK))
        )
    except ClientError as e:
        current_app.logger.error(e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise Conflict('Resource already exists.')
        else:
            raise InternalServerError()
    else:
        return item


def get_item(key):
    try:
        response = get_chat_table().get_item(Key=key)
    except ClientError as e: 
        current_app.logger.error(e)
        raise InternalServerError()
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return None


def query_partition(partition_key):
    try:
        response = get_chat_table().query(
            KeyConditionExpression=Key(PK).eq(partition_key)
        )
    except ClientError as e:
        current_app.logger.error(e)
        raise InternalServerError()
    else:
        if 'Items' in response:
            return response['Items']
        else:
            return []

        
def update_item(item):
    try:
        get_chat_table().put_item(
            Item=item,
            ConditionExpression=('attribute_exists({})'.format(PK))
        )
    except ClientError as e:
        current_app.logger.error(e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise NotFound('Resource not found.')
        else:
            raise InternalServerError()
    else:
        return item
