import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamo_client = boto3.resource("dynamodb")
tweet_analysis_table = dynamo_client.Table("TweetAnalysis")


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
    res = tweet_analysis_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "WeeklyActivity" not in obj:
        return -1.1

    return obj["WeeklyActivity"]
