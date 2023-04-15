"""
Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
"""


import configparser
import csv
import json
import re
import string
from datetime import date
from itertools import repeat
from multiprocessing import Pool

import nltk
import tweepy
from dateutil.relativedelta import relativedelta
from flair.data import Sentence
from flair.models import SequenceTagger, TextClassifier
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

nltk.download("stopwords")
nltk.download("vader_lexicon")


class TwitterClient(object):
    """
    Twitter client class for sentiment analysis
    """

    ## CLASS VARIABLES ##
    # instantiate classifier
    classifier = TextClassifier.load("en-sentiment")

    def __init__(self):
        TwitterClient.setup_config()

    @classmethod
    def read_config(cls):
        """
        Retrieve authentication keys from config file and initialize
        """

        config = configparser.ConfigParser()
        config.read(
            "../config.ini"
        )  # If aws_controller is running, change this to "../config.ini". Otherwise, "../../config.ini"

        cls.ESSENTIAL_KEYS = {
            "api_key": config["twitter-essential"]["api_key"],
            "api_key_secret": config["twitter-essential"]["api_key_secret"],
            "api_access_token": config["twitter-essential"]["access_token"],
            "api_access_token_secret": config["twitter-essential"][
                "access_token_secret"
            ],
            "api_bearer_token": config["twitter-essential"]["bearer_token"],
        }

        cls.ELEVATED_KEYS = {
            "api_key": config["twitter-elevated"]["api_key"],
            "api_key_secret": config["twitter-elevated"]["api_key_secret"],
            "api_access_token": config["twitter-elevated"]["access_token"],
            "api_access_token_secret": config["twitter-elevated"][
                "access_token_secret"
            ],
            "api_bearer_token": config["twitter-elevated"]["bearer_token"],
        }

        # cls.BEARER_TOKEN = config["twitter-essential"]["bearer_token"]

    @classmethod
    def setup_config(cls):
        """
        Set up authentication and initialize client
        """

        cls.read_config()

        ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
        auth = tweepy.OAuthHandler(
            cls.ELEVATED_KEYS["api_key"], cls.ELEVATED_KEYS["api_key_secret"]
        )
        auth.set_access_token(
            cls.ELEVATED_KEYS["api_access_token"],
            cls.ELEVATED_KEYS["api_access_token_secret"],
        )
        cls.api = tweepy.API(auth, wait_on_rate_limit=True)

    @classmethod
    def get_old_tweets(cls, date_since, date_until, type, *search_words):
        """
        Queries past tweets based on provided query and date range and writes them to local files based on date range

        Args:
            date_since (string): Start date from which we want to query the tweets from
            date_until (string): End date to which we want to query the tweets until
            *search_words: Variable argumens for search words (multiple search words are OR'ed by default)

        Returns: None
        """
        cls.setup_config()
        search_string = " OR ".join(search_words)

        tweets = tweepy.Cursor(
            cls.api.search_30_day,
            query=search_string,
            label="thirtyDayEnv",
            fromDate=date_since,
            toDate=date_until,
        ).items(limit=10)

        extracted_tweets = []
        for tweet in tweets:
            tweet_json = {}
            tweet_data = tweet._json
            created_at = str(tweet.created_at)

            tweet_json["Company"] = search_words[0]
            tweet_json["CreatedAndId"] = created_at + "#" + tweet_data["id_str"]
            tweet_json["Text"] = tweet_data["text"]
            tweet_json["TimeRange"] = type

            extracted_tweets.append(tweet_json)

        return extracted_tweets

    @classmethod
    def get_old_weekly_tweets(cls, type, *search_words):
        cls.setup_config()
        search_string = " OR ".join(search_words)

        client = tweepy.Client(cls.ELEVATED_KEYS["api_bearer_token"])
        tweets = client.search_recent_tweets(query=search_string)

        extracted_tweets = []
        for tweet in tweets:
            tweet_json = {}
            tweet_data = tweet._json
            created_at = str(tweet.created_at)

            tweet_json["Company"] = search_words[0]
            tweet_json["CreatedAndId"] = created_at + "#" + tweet_data["id_str"]
            tweet_json["Text"] = tweet_data["text"]
            tweet_json["TimeRange"] = type

            extracted_tweets.append(tweet_json)

        return extracted_tweets

    @classmethod
    def get_activity(cls, *search_words):
        search_string = " OR ".join(search_words)
        client = tweepy.Client(cls.ELEVATED_KEYS["api_bearer_token"])
        counts = client.get_recent_tweets_count(query=search_string)
        most_recent_day_count = counts.data[-1]["tweet_count"]
        most_recent_week_count = counts.meta["total_tweet_count"]

        activity_summary = {
            "company": search_words[0],
            "week_count": most_recent_week_count,
            "day_count": most_recent_day_count,
        }

        return activity_summary

    @classmethod
    def get_news(stock_abbreviation):
        query = stock_abbrevation
        response = []
        i = 0

        return response


# For all tweets beyond one week
def aggregate_all_tweets(client, company, type, start_dates, end_dates):
    tweets = []
    for i in range(0, len(start_dates)):
        tweets += client.get_old_tweets(start_dates[i], end_dates[i], type, *company)
    return tweets


def aggregate_weekly_tweets(client, company, type):
    return client.get_old_weekly_tweets(type, *company)


def aggregate_activity_summary(client, company):
    return client.get_activity(*company)


def get_all_sentiment(tweets):
    sentiments = []
    for tweet in tweets:
        res = get_sentiment(clean(tweet["Text"]))
        sentiments.append(res)

    mean_sentiment = sum(sentiments) / len(sentiments)

    return mean_sentiment


def get_sentiment(tweet):
    """
    For a tweet, obtains sentiment score through Flair API

    Args:
        tweet ([string]): cleaned tokens frm a tweet

    Returns:
        score (string): binary sentiment ('POSITIVE' or 'NEGATIVE')
        confidence (float): confidence level of the result (in range 0-1)

    """
    # > Referenced: https://towardsdatascience.com/text-classification-with-state-of-the-art-nlp-library-flair-b541d7add21f?gi=3675966b8dff
    # sentence = Sentence(tweet)
    sent_analyzer = SentimentIntensityAnalyzer()

    sentence = tweet  # " ".join(tweet)
    sent_dict = sent_analyzer.polarity_scores(sentence)

    return sent_dict["compound"]


def clean(tweet_text):
    """
    Preprocesses/cleans each tweet

    Args:
        tweet_text (string): text content ('text' field) extracted from a single tweet object

    Returns:
        tweets_clean ([string]): array of cleaned tokens from the inputted tweet
    """
    # Remove old style retweet text "RT"
    result = re.sub(r"^RT[\s]", "", tweet_text)
    # Remove links
    result = re.sub("<[a][^>]*>(.+?)</[a]>", "Link.", result)
    # Remove hashtags and other characters
    result = re.sub(r"#", "", result)
    result = re.sub("&gt;", "", result)
    result = re.sub("&#x27;", "'", result)
    result = re.sub("&quot;", '"', result)
    result = re.sub("&#x2F;", " ", result)
    result = re.sub("<p>", " ", result)
    result = re.sub("</i>", "", result)
    result = re.sub("&#62;", "", result)
    result = re.sub("<i>", " ", result)
    result = re.sub("\n", "", result)
    result = re.sub(r"(?i)@[a-z0-9_]+", "", result)

    # instantiate tokenizer class
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    # tokenize tweets
    tweet_tokens = tokenizer.tokenize(result)

    # Import the english stop words list from NLTK
    stopwords_english = stopwords.words("english")

    # Creating a list of words without stopwords
    tweets_clean = []
    for word in tweet_tokens:
        if word not in stopwords_english and word not in string.punctuation:
            tweets_clean.append(word)

    return (" ").join(tweets_clean)


if __name__ == "__main__":
    client = TwitterClient()

    # calculate 6 months ago from today
    today = date.today() + relativedelta(
        days=-1
    )  # subtracting one as we are going from 2/19/23 instead of 2/20/23 to keep it consistent for this week
    six_months = today + relativedelta(months=-6)
    six_months_formatted = six_months.strftime("%Y%m%d%H%M")
    six_months_formatted_start_date = (six_months + relativedelta(weeks=-1)).strftime(
        "%Y%m%d%H%M"
    )

    # calculate last week and the week before if needed
    today_formatted = today.strftime("%Y%m%d%H%M")
    last_week_formatted = (today + relativedelta(weeks=-1)).strftime("%Y%m%d%H%M")
    two_weeks_formatted = (today + relativedelta(weeks=-2)).strftime("%Y%m%d%H%M")

    # calculate last month
    last_month_start_date = today + relativedelta(weeks=-4)
    last_month_start_date_formatted = last_month_start_date.strftime("%Y%m%d%H%M")
    last_month_end_date = last_month_start_date + relativedelta(weeks=1)
    last_month_end_date_formatted = last_month_end_date.strftime("%Y%m%d%H%M")

    # Including cashtags - cashtags aren't available for sandbox/premium twitter dev access.
    search_words = [
        ["#amc"],
        ["#mullen", "#muln"],
        ["#microsoft", "#msft"],
        ["#SPDR", "#spy"],
        ["#disney", "#dis"],
        ["#metamaterials", "#mmat"],
        ["#gamestop", "#gme"],
        ["#nvidia", "#nvda"],
        ["#amazon", "#amzn"],
        ["#c3ai", "#ai"],
        ["#bedbathandbeyond", "#bbby"],
        ["#invesco", "#qqq"],
        ["#google", "#googl", "#alphabet"],
        ["#lyft"],
        ["#dteenergy", "#dte"],
        ["#meta"],
        ["#tesla", "#tsla"],
        ["#apple", "#aapl"],
        ["#netflix", "#nflx"],
    ]

    date_since_arr = [last_month_start_date_formatted, last_week_formatted]
    date_until_arr = [last_month_end_date_formatted, today_formatted]
    # date_since_arr = [two_weeks_formatted]
    # date_until_arr = [last_week_formatted]
    metadata = [True]

    # GET ALL ACTIVITY FOR THE COMPANIES
    # for company in search_words:
    #     client.get_activity(*company)

    # BELOW IS FOR ERROR TRACKING WHEN QUERYING
    # aggregate_all_tweets(
    #     client,
    #     ["$googl", "#google", "#googl", "#alphabet"],
    #     date_since_arr,
    #     date_until_arr,
    # )

    # QUERY PAST TWEETS FOR ALL COMPANIES IN PARALLEL DECREASE RUNTIME AND INCREASE EFFICIENCY
    # Retrieve past tweets in parallel
    with Pool(5) as p:
        p.starmap(
            aggregate_all_tweets,
            zip(
                repeat(client),
                search_words,
                repeat(date_since_arr),
                repeat(date_until_arr),
            ),
        )
