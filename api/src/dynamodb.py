import boto3
import os

from flask import current_app, g

# If you're unfamiliar with DynamoDB I highly recommend watching the following video
# It's long but worth the time IMO: https://www.youtube.com/watch?v=HaEPXoXVf2k

CHAT_DYNAMODB_LOCALHOST_PORT = os.getenv('CHAT_DYNAMODB_LOCALHOST_PORT')
CHAT_DYNAMODB_TABLE_NAME = os.getenv('CHAT_DYNAMODB_TABLE_NAME')

# I'm making using of DynamoDB index overloading so these are generic key attribute names
# See: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html
PARTITION_KEY_ATTRIBUTE_NAME = 'pk'
SORT_KEY_ATTRIBUTE_NAME = 'sk'

def get_chat_table():
    if 'chat_table' not in g:
        dynamodb = get_dynamodb()
        g.chat_table = dynamodb.Table(CHAT_DYNAMODB_TABLE_NAME)


    return g.chat_table

def get_dynamodb():
    if 'dynamodb' not in g:
        g.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://dynamodb:{}".format(CHAT_DYNAMODB_LOCALHOST_PORT),
            region_name="us-east-1"
        )

    return g.dynamodb