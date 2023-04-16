import configparser
import json
import re
import sys
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
        Retrieves news object [title, description, date] as a map
    """

    def get_news(self, stock_abbreviation):
        query = stock_abbreviation
        response = []
        i = 0
        try:
            for submission in self.reddit_read_only.subreddit("wallstreetbets").search(
                query, sort="new", time_filter="month", limit=3
            ):
                if i > 3:
                    break
                if len(submission.selftext) > 0:
                    title = submission.title
                    description = submission.selftext[:180] + "..."
                    description = "".join(description.split("\n"))
                    # convert to May 01, 2023 at 05:15 PM
                    date = dt.utcfromtimestamp(submission.created_utc).strftime(
                        "%B %d, %Y at %I:%M %p"
                    )
                    response.append([title, description, date])
                    i += 1
        except Exception as e:
            return []

        return response

    def get_activity(self, stock_abbreviation):
        query = stock_abbreviation
        activity = 0
        for submission in self.reddit_read_only.subreddit("all").search(
            query, time_filter="month", limit=1000
        ):
            activity += 1
        return activity

    """
      API call to get tweets based on query keyword(s)
    """

    def get_posts(self, stock_abbreviation):
        query = stock
        response = []
        df = pd.DataFrame()

        # retrieve up to 1000 reddit posts
        for submission in self.reddit_read_only.subreddit("all").search(
            query, sort="top", time_filter="month", limit=None
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

    def get_sentiment_to_display(self, stockname):
        query = stockname
        num_submissions = 0
        sentiment = 0

        for submission in self.reddit_read_only.subreddit("all").search(
            query, sort="top", time_filter="month", limit=20
        ):
            confidence, score = self.get_sentiment(
                submission.title + submission.selftext
            )
            num_submissions += 1
            if score == "NEGATIVE":
                confidence *= -1
            sentiment += confidence

        sentiment = sentiment / num_submissions
        return sentiment

    def plottingfunction(x, y, name, show=True):
        # do something with fig and ax here, e.g.
        (line,) = plt.plot(x, y)

        if show:
            plt.show()
        else:
            plt.savefig(name)

        return line


if __name__ == "__main__":
    client = RedditClient()

    n = len(sys.argv)
    print("Total arguments passed:", n)

    # Arguments passed
    print("\nName of Python script:", sys.argv[0])

    print("\nArguments passed:", end=" ")
    stock = "tesla"
    if n >= 2:
        stock = sys.argv[1]

    posts = client.get_posts(stock)

    # number of posts retrieved
    print(len(posts))
    print(posts.head())

    print(dt.fromtimestamp(posts["created_at"].min()).strftime("%Y-%m-%d"))

    # get historical stock data
    tsla = yf.Ticker("TSLA")
    tsla_stock = tsla.history(
        start=dt.fromtimestamp(posts["created_at"].min()).strftime("%Y-%m-%d"),
        end=dt.fromtimestamp(posts["created_at"].max()).strftime("%Y-%m-%d"),
        interval="1d",
    ).reset_index()

    # retrieve dates & remove time zone
    date_times = tsla_stock["Date"]
    date_times = [x.tz_convert(None) for x in date_times]

    def getClosestDate(row):
        res = min(date_times, key=lambda sub: abs(sub - row["date"]))
        return res

    # posts["date_group"] = pd.cut(posts["date"], bins=date_bins, labels=date_times)
    # print(posts.head(100))
    posts["date_group"] = posts.apply(getClosestDate, axis=1)

    def getSentiment(row):
        output = client.get_sentiment(row["text"])
        return output[0] if output[1] == "POSITIVE" else -1 * output[0]

    posts["sentiment"] = posts.apply(getSentiment, axis=1)
    print(posts.iloc[0])
    df = posts.groupby(["date_group"])["sentiment"].mean()

    print(df.head())

    # plot stock data vs. time
    plt.plot(tsla_stock.Date, tsla_stock.Close)
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.title("Stock Price vs. Time")
    # plt.show()
    plt.savefig("stockprice.png")

    # plot sentiment vs. time
    plt.plot(df, color="red")
    plt.xlabel("Time")
    plt.ylabel("Avg Sentiment Score")
    plt.title("Avg Sentiment vs. Time")
    # plt.show()
    plt.savefig("sentiment.png")

    print(df.head(20))

    # df.plot(x="date_group", y="unemployment_rate", kind="line")

    # df = posts.groupby(pd.cut(posts["created_at"], bins=7)).apply(lambda x: x[t])
    # print(df.head())
