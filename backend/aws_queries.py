import hashlib
from datetime import datetime as dt

import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

dynamo_client = boto3.resource("dynamodb")
tweet_analysis_table = dynamo_client.Table("TweetAnalysis")
tweet_table = dynamo_client.Table("Tweets")
users_table = dynamo_client.Table("Users")


def get_weekly_sentiment_score_by_company(company):
    res = tweet_analysis_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "1_SentimentScore" not in obj:
        return -1.1

    return obj["1_SentimentScore"]


def get_two_weeks_sentiment_score_by_company(company):
    res = tweet_analysis_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "2_SentimentScore" not in obj:
        return -1.1

    return obj["2_SentimentScore"]


def get_monthly_sentiment_score_by_company(company):
    # company = "#" + company.lower()
    res = tweet_analysis_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "3_SentimentScore" not in obj:
        return -1.1

    return obj["3_SentimentScore"]


def get_activity_by_company(company):
    # company = "#" + company.lower()
    res = tweet_analysis_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "WeeklyActivity" not in obj:
        return -1.1

    return obj["WeeklyActivity"]


def get_tweets_by_company(company):
    ret = []
    company = "#" + company.lower()
    res = tweet_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "CreatedAndId" not in obj:
        return -1.1

    res_sorted = sorted(
        res["Items"], key=lambda item: item["CreatedAndId"], reverse=True
    )

    # append the first tweet.
    date_arr = res_sorted[0]["CreatedAndId"].split(" ")
    date_arr[1] = date_arr[1].split("+")[0]
    date = dt.strptime(date_arr[0], "%Y-%m-%d").strftime("%B %d, %Y")
    time = dt.strptime(date_arr[1], "%H:%M:%S").strftime("%I:%M %p")
    text_arr = res_sorted[0]["Text"].split(": ")
    ret.append([text_arr[0], "".join(text_arr[1:]), date + " at " + time])

    i = 0
    while len(ret) < 3:
        i += 1
        if res_sorted[i]["Text"].split(": ")[0] == ret[-1][0]:
            continue
        date_arr = res_sorted[i]["CreatedAndId"].split(" ")
        date_arr[1] = date_arr[1].split("+")[0]
        date = dt.strptime(date_arr[0], "%Y-%m-%d").strftime("%B %d, %Y")
        time = dt.strptime(date_arr[1], "%H:%M:%S").strftime("%I:%M %p")
        text_arr = res_sorted[i]["Text"].split(": ")
        ret.append([text_arr[0], "".join(text_arr[1:]), date + " at " + time])

    return ret


def login_user(email, password):
    hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
    try:
        res = users_table.query(
            KeyConditionExpression=Key("Email").eq(email),
        )
        if len(res["Items"]) == 0:
            return {"code": 404}
        else:
            user = res["Items"][0]
            if user["HashedPassword"] != hashed_password:
                return {"code": 401}
            else:
                return {
                    "code": 200,
                    "username": user["Username"],
                    "watchlist": user["WatchList"],
                }
    except ClientError as err:
        print("Couldn't add a new user. Here's why: ")
        print(err.response["Error"]["Code"])
        print(": " + err.response["Error"]["Message"])
        raise


def get_company_analytics(company):
    company = "#" + company.lower()
    print(company)
    try:
        res = tweet_analysis_table.query(
            KeyConditionExpression=Key("Company").eq(company),
        )
        return res["Items"][0]
    except ClientError as err:
        print("Couldn't add a new user. Here's why: ")
        print(err.response["Error"]["Code"])
        print(": " + err.response["Error"]["Message"])
        raise
