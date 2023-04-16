import sys
from decimal import Decimal

sys.path.append("../../")
import io
import re

import app.analysis.reddit_client as rc
import app.analysis.timeframes as time
import app.analysis.twitter_client as tw
import boto3
import emoji
import matplotlib.pyplot as plt
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from wordcloud import WordCloud

dynamo_client = boto3.resource("dynamodb")
reddit_analysis_table = dynamo_client.Table("RedditAnalysis")

s3_source = boto3.resource("s3")
s3_client = boto3.client("s3")
bucket = s3_source.Bucket("redditwordcloud")

"""
    READ and WRITE functions to DynamoDB resources related to Reddit
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


def get_reddit_texts_by_company(company):
    """
    Queries tweets texts from Tweets table by the partition key (Company) and by type, which indicates the timeframe (past week or past month)

    Args:
        company (string): name of the company interested in
        type (int): timeframe (As of now, 1 = week, 2 = months)

    Returns: List of tweets
    """
    client = rc.RedditClient()
    posts = client.get_posts(company)

    return [
        re.sub(r"\s*http(.*)", "", tw.clean(emoji.replace_emoji(i["text"], replace="")))
        for i in posts
        if "text" in i
    ]


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

        key = company + ".png"
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


if __name__ == "__main__":
    # batch_write_tweets_to_tweets_table()
    # entries = store_data_analysis_for_all_companies()
    # batch_write_analytics_to_tweet_analysis_table(entries)
    # store_word_cloud_for_past_week()
    posts = get_reddit_texts_by_company("googl")
    console.log(posts)
