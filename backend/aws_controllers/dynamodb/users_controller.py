import sys
from decimal import Decimal

sys.path.append("..")
import hashlib
from datetime import datetime
from uuid import uuid4

import app.analysis.timeframes as time
import app.analysis.twitter_client as tw
import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

dynamo_client = boto3.resource("dynamodb")
users_table = dynamo_client.Table("Users")

"""
    READ and WRITE functions to DynamoDB resources related to Users
"""


def register_user(username, password, email):
    hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
    user_id = datetime.now().strftime("%Y%m%d%H%M%S-") + str(uuid4())
    try:
        users_table.put_item(
            Item={
                "UserId": user_id,
                "Username": username,
                "Email": email,
                "HashedPassword": hashed_password,
            },
            ConditionExpression="attribute_not_exists(Email)",
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"code": 409}

        print("Couldn't add a new user. Here's why: ")
        print(err.response["Error"]["Code"])
        print(": " + err.response["Error"]["Message"])
        raise
    return ""


if __name__ == "__main__":
    pass
