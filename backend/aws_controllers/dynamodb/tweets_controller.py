import sys
from decimal import Decimal

sys.path.append("../../")
import collections
import io
import re

import app.analysis.timeframes as time
import app.analysis.twitter_client as tw
import boto3
import emoji
import matplotlib.pyplot as plt
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from dateutil import parser
from langdetect import detect
from wordcloud import WordCloud

dynamo_client = boto3.resource("dynamodb")
tweets_table = dynamo_client.Table("Tweets")
tweet_analysis_table = dynamo_client.Table("TweetAnalysis")

s3_source = boto3.resource("s3")
s3_client = boto3.client("s3")
bucket = s3_source.Bucket("tweetwordcloud")
tweet_sentiment_freq_bucket = s3_source.Bucket("tweetsentimentfreq")
tweet_sentiment_change_bucket = s3_source.Bucket("tweetsentimentchange")

"""
    READ and WRITE functions to DynamoDB resources related to Tweets
"""

COMPANIES = [
    ["#amc"],
    ["#muln", "#mullen"],
    ["#googl", "#alphabet", "#google"],
    ["#meta"],
    ["#tsla", "#tesla"],
    ["#aapl", "#apple"],
    ["#nflx", "#netflix"],
    ["#amzn", "#amazon"],
    ["#msft", "#microsoft"],
    ["#spy", "#SPDR"],
    ["#dis", "#disney"],
    ["#mmat", "#metamaterials"],
    ["#gme", "#gamestop"],
    ["#ai", "#c3ai"],
    ["#bbby", "#bedbathandbeyond"],
    ["#qqq", "#invesco"],
    ["#lyft"],
    ["#dte", "#dteenergy"],
]


# Until Lambda gets set up, we need to manually update
# `dates_since_arr`, `dates_until_arr` with the timeframes
# we are interested in. We also need to change line 25 with
# the company we want to query tweets about.
def batch_write_tweets_to_tweets_table():
    client = tw.TwitterClient()

    last_month = time.get_one_month_ago_range()
    last_week = time.get_week_ago_range()
    last_two_weeks = time.get_two_weeks_ago_range()

    date_since_arr = last_week["dates_since"]
    date_until_arr = last_week["dates_until"] * len(date_since_arr)
    # type = 1 for last week and type = 2 for last month, type = 3 for two weeks
    # Eventually, data in last week would become part of last month so that we avoid querying for the same data multiple times
    type = 1

    for company in COMPANIES:
        table_data = tw.aggregate_all_tweets(
            client,
            company,
            type,
            date_since_arr,
            date_until_arr,
        )
        # print(table_data)

        try:
            with tweets_table.batch_writer() as writer:
                for item in table_data:
                    writer.put_item(Item=item)
            print("Loaded data into table %s.", tweets_table.name)
        except ClientError:
            print("Couldn't load data into table %s.", tweets_table.name)
            raise


def get_tweets_by_company(company, type):
    """
    Queries tweets from Tweets table by the partition key (Company) and by type, which indicates the timeframe (past week or past month)

    Args:
        company (string): name of the company interested in
        type (int): timeframe (As of now, 1 = week, 2 = months)

    Returns: List of tweets
    """

    res = tweets_table.query(
        KeyConditionExpression=Key("Company").eq(company),
        FilterExpression=Attr("TimeRange").eq(type),
    )

    return res["Items"]


def get_tweets_texts_by_company(company, type):
    """
    Queries tweets texts from Tweets table by the partition key (Company) and by type, which indicates the timeframe (past week or past month)

    Args:
        company (string): name of the company interested in
        type (int): timeframe (As of now, 1 = week, 2 = months)

    Returns: List of tweets
    """

    res = tweets_table.query(
        KeyConditionExpression=Key("Company").eq(company),
        FilterExpression=Attr("TimeRange").eq(type),
    )

    texts = []
    for i in res["Items"]:
        if "Text" in i:
            text = i["Text"]
            try:
                en = detect(text) == "en"
                if en:
                    texts.append(
                        re.sub(
                            r"\s*http(.*)",
                            "",
                            tw.clean(emoji.replace_emoji(text, replace="")),
                        )
                    )
            except:
                language = "error"
                print("This row throws an error")
    return texts


def batch_write_analytics_to_tweet_analysis_table(entries):
    """
    Batch writes passed in entry for each company and its sentiment scores + other necessary data to TweetAnalysis table

    Args:
        entries (list): List of dictionaries, where each dictionary holds Company,
                        TimeRange (aka type -> 1 if past week, 2 if past month), StartDate
                        and EndDate of TimeRange, and SentimentScore
    Returns: Nothing
    """

    try:
        with tweet_analysis_table.batch_writer() as writer:
            for item in entries:
                writer.put_item(Item=item)
        print("Loaded data into table %s.", tweet_analysis_table.name)
    except ClientError:
        print("Couldn't load data into table %s.", tweet_analysis_table.name)
        raise


def calculate_sentiment_score(company, type, tweets):
    """
    Calculates mean sentiment scores of the given tweets

    Args:
        company (String): company name
        type (int): 1 if past week, 2 if last month
        tweets (list): list of all queried tweets from Tweets table
    Returns: Decimal value of the mean sentiment score
    """
    mean_sentiment = tw.get_all_sentiment(tweets)

    entry = {}
    entry["Company"] = company

    # NOTE: Extract out the date. Should be by @ with the new data
    start_date = "".join(tweets[0]["CreatedAndId"].split("#")[0])
    end_date = "".join(tweets[-1]["CreatedAndId"].split("#")[0])

    entry["StartDate"] = start_date
    entry["EndDate"] = end_date
    entry["SentimentScore"] = Decimal(str(mean_sentiment))

    return entry


def store_data_analysis_for_all_companies():
    """
    Entire flow of querying for tweets, calculating their mean scores, and creating an
    entry with necessary data for each company to be stored in TweetAnalysis table

    Args:
        type (int): 1 if past week, 2 if last month
    Returns: Decimal value of the mean sentiment score
    """

    companies = [
        # "#amc",
        # "#muln",
        "#googl",
        # "#meta",
        # "#tsla",
        # "#aapl",
        # "#nflx",
        # "#amzn",
        # "#msft",
        # "#spy",
        # "#dis",
        # "#mmat",
        # "#gme",
        # "#ai",
        # "#bbby",
        # "#qqq",
        # "#lyft",
        # "#dte",
    ]

    client = tw.TwitterClient()

    entries = []
    for company in COMPANIES:
        entry = {}
        entry["Company"] = company[0]
        for i in [1, 2, 3]:
            tweets = get_tweets_by_company(company[0], i)
            if len(tweets) > 0:
                res = calculate_sentiment_score(company[0], i, tweets)
                start_date_label = str(i) + "_StartDate"
                end_date_label = str(i) + "_EndDate"
                sentiment_score_label = str(i) + "_SentimentScore"

                entry[start_date_label] = res["StartDate"]
                entry[end_date_label] = res["EndDate"]
                entry[sentiment_score_label] = res["SentimentScore"]

        activity_res = tw.aggregate_activity_summary(client, company)
        entry["WeeklyActivity"] = activity_res["week_count"]
        entry["DailyActivity"] = activity_res["day_count"]
        entries.append(entry)

    return entries


def store_change_in_sentiment_score_for_past_week():
    companies = [
        "#amc",
        "#muln",
        "#googl",
        "#meta",
        "#tsla",
        "#aapl",
        "#nflx",
        "#amzn",
        "#msft",
        "#spy",
        "#dis",
        "#mmat",
        "#gme",
        "#ai",
        "#bbby",
        "#qqq",
        "#lyft",
        "#dte",
    ]

    expiration = 604800
    for company in companies:
        res = tweet_analysis_table.query(
            KeyConditionExpression=Key("Company").eq(company),
        )

        item = res["Items"][0]

        x_axis = []
        y_axis = []
        if "1_StartDate" in item:
            date_1_start = parser.parse(item["1_StartDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            date_1_end = parser.parse(item["1_EndDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            x_axis.append(date_1_start + " ~ " + date_1_end)
            y_axis.append(float(item["1_SentimentScore"]) * 100)

        if "2_StartDate" in item:
            date_1_start = parser.parse(item["2_StartDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            date_1_end = parser.parse(item["2_EndDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            x_axis.append(date_1_start + " ~ " + date_1_end)
            y_axis.append(float(item["2_SentimentScore"]) * 100)

        if "3_StartDate" in item:
            date_1_start = parser.parse(item["3_StartDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            date_1_end = parser.parse(item["3_EndDate"].split("#")[0]).strftime(
                "%Y-%m-%d"
            )
            x_axis.append(date_1_start + " ~ " + date_1_end)
            y_axis.append(float(item["3_SentimentScore"]) * 100)

        key = company + "_sentiment_change.png"

        plt.plot(x_axis, y_axis)
        plt.title("Change in Sentiment Score")
        plt.xlabel("Date Range")
        plt.ylabel("Sentiment Score")

        fig1 = plt.gcf()
        plt.show()
        fig1.savefig(key, bbox_inches="tight")
        plt.close()

        img_data = io.BytesIO()
        fig1.savefig(img_data, format="png")
        img_data.seek(0)

        tweet_sentiment_change_bucket.put_object(
            Body=img_data, ContentType="image/png", Key=key
        )

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": "tweetsentimentchange", "Key": key},
                ExpiresIn=expiration,
            )

            try:
                tweet_analysis_table.update_item(
                    Key={"Company": company},
                    # UpdateExpression="SET Watchlist = list_append(Watchlist, :i)",
                    UpdateExpression="SET SentimentScoreChangeGraph=:w",
                    ExpressionAttributeValues={
                        ":w": url,
                    },
                    ReturnValues="UPDATED_NEW",
                )
            except ClientError as err:
                print("Couldn't add a new user. Here's why: ")
                print(err.response["Error"]["Code"])
                print(": " + err.response["Error"]["Message"])
                raise

        except ClientError as e:
            print(e)
            return None


def store_sentiment_frequency_for_past_week():
    companies = [
        "#amc",
        "#muln",
        "#googl",
        "#meta",
        "#tsla",
        "#aapl",
        "#nflx",
        "#amzn",
        "#msft",
        "#spy",
        "#dis",
        "#mmat",
        "#gme",
        "#ai",
        "#bbby",
        "#qqq",
        "#lyft",
        "#dte",
    ]

    expiration = 604800
    for company in companies:
        sentiments = []
        tweet_texts = get_tweets_texts_by_company(company, 1)
        if len(tweet_texts) == 0:
            continue
        for tweet in tweet_texts:
            sentiments.append(round(tw.get_sentiment(tw.clean(tweet)), 1))

        c = collections.Counter(sentiments)
        c = sorted(c.items())
        scores = [
            -1.0,
            -0.9,
            -0.8,
            -0.7,
            -0.6,
            -0.5,
            -0.4,
            -0.3,
            -0.2,
            -0.1,
            0,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1,
        ]

        key = company + "_sentiment_freq.png"

        freq = [i[1] for i in c]
        freq_num = [i[0] for i in c]
        f, ax = plt.subplots()

        plt.bar(freq_num, freq, width=0.05, facecolor="black", edgecolor="black")
        plt.title("Sentiment Score Distribution")
        plt.xlabel("Scores")
        plt.ylabel("Frequency")
        ax.set_xticks(scores)
        ax.set_xticklabels([str(label) for label in scores])

        fig1 = plt.gcf()
        plt.show()
        fig1.savefig(key, bbox_inches="tight")
        plt.close()

        img_data = io.BytesIO()
        fig1.savefig(img_data, format="png")
        img_data.seek(0)

        tweet_sentiment_freq_bucket.put_object(
            Body=img_data, ContentType="image/png", Key=key
        )

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": "tweetsentimentfreq", "Key": key},
                ExpiresIn=expiration,
            )

            try:
                tweet_analysis_table.update_item(
                    Key={"Company": company},
                    # UpdateExpression="SET Watchlist = list_append(Watchlist, :i)",
                    UpdateExpression="SET SentimentFreqBarChart=:w",
                    ExpressionAttributeValues={
                        ":w": url,
                    },
                    ReturnValues="UPDATED_NEW",
                )
            except ClientError as err:
                print("Couldn't add a new user. Here's why: ")
                print(err.response["Error"]["Code"])
                print(": " + err.response["Error"]["Message"])
                raise

        except ClientError as e:
            print(e)
            return None


def store_word_cloud_for_past_week():
    companies = [
        "#amc",
        "#muln",
        "#googl",
        "#meta",
        "#tsla",
        "#aapl",
        "#nflx",
        "#amzn",
        "#msft",
        "#spy",
        "#dis",
        "#mmat",
        "#gme",
        "#ai",
        "#bbby",
        "#qqq",
        "#lyft",
        "#dte",
    ]

    expiration = 604800
    for company in companies:
        tweet_texts = get_tweets_texts_by_company(company, 1)
        if len(tweet_texts) == 0:
            continue
        unique_string = (" ").join(tweet_texts)
        wordcloud = WordCloud(width=1000, height=500).generate(unique_string)
        key = company + ".png"
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        fig1 = plt.gcf()
        plt.show()
        fig1.savefig(key, bbox_inches="tight")
        plt.close()

        img_data = io.BytesIO()
        fig1.savefig(img_data, format="png")
        img_data.seek(0)

        bucket.put_object(Body=img_data, ContentType="image/png", Key=key)

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": "tweetwordcloud", "Key": key},
                ExpiresIn=expiration,
            )

            try:
                tweet_analysis_table.update_item(
                    Key={"Company": company},
                    # UpdateExpression="SET Watchlist = list_append(Watchlist, :i)",
                    UpdateExpression="SET WordCloud=:w",
                    ExpressionAttributeValues={
                        ":w": url,
                    },
                    ReturnValues="UPDATED_NEW",
                )
            except ClientError as err:
                print("Couldn't add a new user. Here's why: ")
                print(err.response["Error"]["Code"])
                print(": " + err.response["Error"]["Message"])
                raise

        except ClientError as e:
            print(e)
            return None


def update_outdated_tweets_table():
    response = tweets_table.scan()
    data = response["Items"]
    for item in data:
        company = item["Company"]
        createdAndId = item["CreatedAndId"]
        if not hasattr(item, "TimeRange"):
            continue
        prev_timerange = item["TimeRange"]
        tweets_table.update_item(
            Key={"Company": company, "CreatedAndId": createdAndId},
            # UpdateExpression="SET Watchlist = list_append(Watchlist, :i)",
            UpdateExpression="SET TimeRange=:tr",
            ExpressionAttributeValues={
                ":tr": prev_timerange + 1,
            },
            ReturnValues="UPDATED_NEW",
        )


if __name__ == "__main__":
    # batch_write_tweets_to_tweets_table()

    # entries = store_data_analysis_for_all_companies()
    # batch_write_analytics_to_tweet_analysis_table(entries)

    # store_word_cloud_for_past_week()
    # store_sentiment_frequency_for_past_week()
    store_change_in_sentiment_score_for_past_week()

    # update_outdated_tweets_table()
