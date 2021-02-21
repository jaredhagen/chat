"""
This module contains functions with a simplified interface for adding, updating and
retrieving items from DynamoDB. With error handling that throws appropriate HTTP
exceptions.
"""
import time

import boto3

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import current_app, g
from werkzeug.exceptions import Conflict, InternalServerError, NotFound


# If you're unfamiliar with DynamoDB I highly recommend watching the  following video.
# It's long but worth the time IMHO.
# See: https://www.youtube.com/watch?v=HaEPXoXVf2k

# I'm making using of DynamoDB index overloading so these are generic key attribute
# names.
# See: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html
PK = "pk"
SK = "sk"

# I'm using a constant value for the users and rooms partition keys since this dynamodb
# table is currently single tenent. If the table was multitenent I would use an account
# id or something along those lines to partition the users and rooms by account.  If I
# were to expect these lists to get too large or to be too "hot" I would implement a
# sharding strategy.
# See: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-sharding.html pylint: disable=C0301
USER_PARTITION_KEY = "users"
ROOM_PARTITION_KEY = "rooms"


def epoch_time():
    """
    Return a UNIX timestamp in milliseconds.  Used for setting the created_at attribute
    on a Message and the last_active_at attribute on a Room
    """
    return int(time.time() * 1000)


def get_dynamodb():
    """
    Used to get an instance of the DynamoDB client. The endpoint_url can be configured
    using the CHAT_DYNAMODB_ENDPOINT_URL environment variable. When connecting to an AWS
    managed DynamoDB instance the endpoint_url should not be specified and instead the
    boto3.resource function should only be passed a region.
    """
    if "dynamodb" not in g:
        endpoint_url = current_app.config["CHAT_DYNAMODB_ENDPOINT_URL"]
        g.dynamodb = boto3.resource(
            "dynamodb", endpoint_url=endpoint_url, region_name="us-east-1"
        )

    return g.dynamodb


def get_chat_table():
    """
    Used to get an instance of the application Table to perform queries with. The table
    name can be configured using the CHAT_DYNAMODB_TABLE_NAME environment variable.
    """
    if "chat_table" not in g:
        table_name = current_app.config["CHAT_DYNAMODB_TABLE_NAME"]
        dynamodb = get_dynamodb()
        g.chat_table = dynamodb.Table(table_name)

    return g.chat_table


def add_item(item):
    """
    Used to add an item to the dynamodb table. The condition expression ensures that we
    don't overrite any existing records in the table.  If the condition expression isn't
    met a response with a 409 status code is returned.
    """
    try:
        get_chat_table().put_item(
            Item=item, ConditionExpression=("attribute_not_exists({})".format(PK))
        )
    except ClientError as error:
        if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise Conflict("Resource already exists.")  # pylint: disable=W0707
        current_app.logger.error(error)
        raise InternalServerError() from error
    else:
        return item


def get_item(key):
    """
    Used to get an individual item from the dynamodb table. If there is no item with the
    given key None is returned.
    """
    try:
        response = get_chat_table().get_item(Key=key)
    except ClientError as error:
        current_app.logger.error(error)
        raise InternalServerError() from error
    else:
        if "Item" in response:
            return response["Item"]
        return None


def query_partition(partition_key, limit=None, scan_index_forward=True):
    """
    Used to get all items in a partition (all items that have the same PK attribute).

    Limit - limits the number of records that DynamoDB processes before returning not
    the number of items that are returned.  Fortunately this distinction doesn't matter
    for our data. This is used when retrieving all rooms and messages within a room.

    ScanIndexForward - Tells DynamoDB in which order to read the items in the partition.
    When retrieving messages scan_index_forward should be False so the latest messages
    are returned.

    See: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query pylint: disable=C0301
    """
    try:
        fun_kwargs = {"Limit": limit} if limit else {}
        response = get_chat_table().query(
            KeyConditionExpression=Key(PK).eq(partition_key),
            ScanIndexForward=scan_index_forward,
            **fun_kwargs
        )
    except ClientError as error:
        current_app.logger.error(error)
        raise InternalServerError() from error
    else:
        if "Items" in response:
            return response["Items"]
        return []


def update_item(item):
    """
    Used to update an item in the dynamodb table. This function performs a full replace
    of the item.  DynamoDB has support for partial updates but that is currently not
    needed by the application. The condition expression ensures that we don't create a
    new record in the table. If the condition expression isn't met a response with a 404
     status code is returned.
    """
    try:
        get_chat_table().put_item(
            Item=item, ConditionExpression=("attribute_exists({})".format(PK))
        )
    except ClientError as error:
        if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise NotFound("Resource not found.")  # pylint: disable=W0707
        current_app.logger.error(error)
        raise InternalServerError() from error
    else:
        return item
