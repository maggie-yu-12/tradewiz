import boto3
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime as dt

dynamo_client = boto3.resource("dynamodb")
tweet_analysis_table = dynamo_client.Table("TweetAnalysis")
tweet_table = dynamo_client.Table("Tweets")


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

def get_tweets_by_company(company):
    ret = []
    company = "#" + company.lower()
    res = tweet_table.query(
        KeyConditionExpression=Key("Company").eq(company),
    )
    print("THIS IS THE RES", res["Items"][:4])

    if len(res["Items"]) == 0:
        return -1.1

    obj = res["Items"][0]
    if "CreatedAndId" not in obj:
        return -1.1


    res_sorted = sorted(res["Items"], key=lambda item:item["CreatedAndId"], reverse=True)
    print("THIS IS SORTED RES", res_sorted[:4])

    # append the first tweet.
    date_arr = res_sorted[0]["CreatedAndId"].split(" ")
    date_arr[1] = date_arr[1].split("+")[0]
    date = dt.strptime(date_arr[0], "%Y-%m-%d").strftime("%B %d, %Y")
    time = dt.strptime(date_arr[1], "%H:%M:%S").strftime("%I:%M %p")
    text_arr = res_sorted[0]["Text"].split(": ")
    ret.append([text_arr[0], ''.join(text_arr[1:]), date + " at " + time])

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
        ret.append([text_arr[0], ''.join(text_arr[1:]), date + " at " + time])
    
    return ret
