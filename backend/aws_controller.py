import app.analysis.timeframes as time
import app.analysis.twitter_client as tw
import boto3
from botocore.exceptions import ClientError

dynamo_client = boto3.resource("dynamodb")
table = dynamo_client.Table("Tweets")


# Until Lambda gets set up, we need to manually update
# `dates_since_arr`, `dates_until_arr` with the timeframes
# we are interested in. We also need to change line 25 with
# the company we want to query tweets about.
def batch_write_tweets_to_tweets_table():
    client = tw.TwitterClient()

    last_month = time.get_one_month_ago_range()
    last_week = time.get_week_ago_range()

    date_since_arr = last_month["dates_since"]
    date_until_arr = last_month["dates_until"] * len(date_since_arr)
    # type = 1 for last week and type = 2 for last month
    # Eventually, data in last week would become part of last month so that we avoid querying for the same data multiple times
    type = 2

    companies = [
        # ["#amc"],
        # ["#muln", "#mullen"],
        # ["#googl", "#alphabet", "#google"],
        # ["#meta"],
        ["#tsla", "#tesla"],
        ["#aapl", "#apple"],
        # ["#nflx", "#netflix"],
        ["#amzn", "#amazon"],
        ["#msft", "#microsoft"],
        # ["#spy", "#SPDR"],
        # ["#dis", "#disney"],
        # ["#mmat", "#metamaterials"],
        # ["#gme", "#gamestop"],
        ["#nvda", "#nvidia"],
        ["#amzn", "#amazon"],
        # ["#ai", "#c3ai"],
        # ["#bbby", "#bedbathandbeyond"],
        # ["#qqq", "#invesco"],
        # ["#lyft"],
        # ["#dte", "#dteenergy"],
    ]

    for company in companies:
        table_data = tw.aggregate_all_tweets(
            client,
            company,
            type,
            date_since_arr,
            date_until_arr,
        )

        try:
            with table.batch_writer() as writer:
                for item in table_data:
                    writer.put_item(Item=item)
            print("Loaded data into table %s.", table.name)
        except ClientError:
            print("Couldn't load data into table %s.", table.name)
            raise


if __name__ == "__main__":
    batch_write_tweets_to_tweets_table()
