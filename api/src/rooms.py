import functools
import os
import ulid

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from flask import (
    Blueprint, g, redirect, request
)

from src.dynamodb import get_chat_table, PARTITION_KEY_ATTRIBUTE_NAME, SORT_KEY_ATTRIBUTE_NAME

# I'm using a constant value for the rooms partition key since this dynamodb table is currently single tenent
# If the table was multitenent I would use an account id or something along those lines to partition the rooms
ROOM_PARTITION_KEY = 'room'

bp = Blueprint('rooms', __name__, url_prefix='/rooms')


@bp.route('', methods=['POST'])
def create_room():
    id = str(ulid.new())
    name = request.json['name']

    response = get_chat_table().put_item(
        Item={
            PARTITION_KEY_ATTRIBUTE_NAME: ROOM_PARTITION_KEY,
            SORT_KEY_ATTRIBUTE_NAME: id,
            'name': request.json['name']
        }
    )
    return {
        'id': id,
        'name': name
    }


@bp.route('', methods=['GET'])
def get_rooms():
    response = get_chat_table().query(
        KeyConditionExpression=Key(PARTITION_KEY_ATTRIBUTE_NAME).eq(ROOM_PARTITION_KEY)
    )
    return {
        'rooms': response['Items']
    }


@bp.route('/<room_id>', methods=['GET'])
def get_room(room_id):
    try:
        response = get_chat_table().get_item(
            Key={
                PARTITION_KEY_ATTRIBUTE_NAME: 'rooms',
                SORT_KEY_ATTRIBUTE_NAME: room_id
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return "404 Not Found"
    return response
