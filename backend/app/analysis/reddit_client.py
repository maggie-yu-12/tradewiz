import configparser
import json
import re
from datetime import datetime as dt
from datetime import timedelta

import flair
import matplotlib.pyplot as plt
import pandas as pd
import praw
import yfinance as yf
from client import Client
from flair.data import Sentence
from flair.models import SequenceTagger, TextClassifier


class RedditClient(Client):
    """
    Reddit client class for sentiment analysis
    """

    def __init__(self):
        """
        Set up authentication and initialize client
        """
        self.sentiment_model = flair.models.TextClassifier.load("en-sentiment")

        # Read-only instance
        self.reddit_read_only = praw.Reddit(
            client_id="jR-4thKK9gWzUeWbmoMnXQ",
            client_secret="5N8JI3jtN0Jn56CrXpLfkLBDulnCeQ",
            user_agent="retrieve_wallstreetbets_content",
        )

        # self.subreddit = reddit_read_only.subreddit("wallstreetbets")

        # print("Display Name:", self.subreddit.display_name)

        # Display the title of the Subreddit
        # print("Title:", self.subreddit.title)

    def get_data(self, submission):
        data = pd.DataFrame(
            {
                "id": [submission.id],
                "created_at": [submission.created_utc],
                "date": [dt.fromtimestamp(submission.created_utc)],
                "text": [submission.selftext + submission.title],
            }
        )
        return data

    """
      API call to get tweets based on query keyword(s)
    """

    def get_posts(self):
        query = "tesla"
        response = []
        df = pd.DataFrame()

        for submission in self.reddit_read_only.subreddit("all").search(
            query, sort="top", time_filter="week"
        ):
            # print(submission.selftext)
            df = df.append(self.get_data(submission), ignore_index=True)
            response.append(submission.title + submission.selftext)

        return df

    def get_sentiment(self, tweet):
        """
        For a tweet, obtains sentiment score through Flair API
        Args:
            tweet ([string]): cleaned tokens frm a tweet
        Returns:
            score (string): binary sentiment ('POSITIVE' or 'NEGATIVE')
            confidence (float): confidence level of the result (in range 0-1)

        """
        # > Referenced: https://towardsdatascience.com/text-classification-with-state-of-the-art-nlp-library-flair-b541d7add21f?gi=3675966b8dff
        sentence = Sentence(tweet)
        x = self.sentiment_model.predict(sentence)

        return sentence.labels[0].score, sentence.labels[0].value


if __name__ == "__main__":
    client = RedditClient()
    posts = client.get_posts()
    print(len(posts))
    print(posts.head())
    # for i in range(2):
    # print("sentiment score: ", client.get_sentiment(posts[i]), posts[i])

    # get historical stock data
    tsla = yf.Ticker("TSLA")
    tsla_stock = tsla.history(
        start=dt.fromtimestamp(posts["created_at"].min()).strftime("%Y-%m-%d"),
        end=dt.fromtimestamp(posts["created_at"].max()).strftime("%Y-%m-%d"),
        interval="60m",
    ).reset_index()
    # print(tsla_stock)

    date_times = tsla_stock["Datetime"]
    print(date_times)

    date_bins = [d - timedelta(hours=0, minutes=30) for d in date_times]
    date_bins.append(date_times.iloc[-1] + timedelta(hours=0, minutes=30))
    print(date_bins)

    posts["date_group"] = pd.cut(posts["date"], bins=date_bins, labels=date_times)
    print(posts.head(100))

    def getSentiment(row):
        output = client.get_sentiment(row["text"])
        return output[0] if output[1] == "POSITIVE" else -1 * output[0]

    posts["sentiment"] = posts.apply(getSentiment, axis=1)

    # plot stock data vs. time
    plt.plot(tsla_stock.Datetime, tsla_stock.Close)
    plt.show()

    df = posts.groupby(["date_group"])["sentiment"].mean()
    # print(df.head())

    # df.plot(x="date_group", y="unemployment_rate", kind="line")

    # df = posts.groupby(pd.cut(posts["created_at"], bins=7)).apply(lambda x: x[t])
    # print(df.head())
