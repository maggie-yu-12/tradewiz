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
from itertools import repeat
from multiprocessing import Pool

import nltk
import requests
import tweepy
from flair.data import Sentence
from flair.models import SequenceTagger, TextClassifier
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

nltk.download("stopwords")


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
        config.read("../../config.ini")

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

        # self.BEARER_TOKEN = config['twitter-essential']['bearer_token']

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
    def get_old_tweets(cls, date_since, date_until, prev_week, *search_words):
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

        # Create a name for file that we will be writing tweets to
        filename = (
            "past_tweets_for_"
            + search_string
            + "_"
            + date_since
            + "_"
            + date_until
            + ".txt"
        )

        # UNCOMMENT TO RUN THE QUERIES
        # !! NOTE: WE NEED TO BE CAREFUL BC WE CAN run AT MAX 50 QUERIES PER MONTH :((
        tweets = tweepy.Cursor(
            cls.api.search_full_archive,
            query=search_string,
            label="fullArchiveEnviron",
            fromDate=date_since,
            toDate=date_until,
        ).items(limit=10)

        filepath = "queried_data/" + filename
        with open(filepath, "w") as file:
            for elem in tweets:
                # Turn Status (`elem` data type) object into a JSON format to make writable to a file
                s = json.dumps(elem._json)
                file.write(s)
                file.write("\n")

        # store all sentiments for the week
        cls.get_all_sentiment(
            filepath, prev_week, search_words[0], date_since, date_until
        )

    @classmethod
    def get_all_sentiment(cls, filepath, prev_week, company, date_since, date_until):
        # Reads in files with past tweets and extracts out text from each
        queried_tweets = []
        with open(filepath, "r") as file:
            for line in file:
                obj = json.loads(line)
                queried_tweets.append(obj["text"])

        sentiments = []
        for tweet in queried_tweets:
            sentiments.append(cls.get_sentiment(cls.clean(tweet))[1])

        mean_sentiment = sum(sentiments) / len(sentiments)

        # filename_no_txt = filename.rsplit(".", 1)[0]
        csv_filename = "prev_week.csv" if prev_week else "curr_week.csv"
        with open(csv_filename, "a", newline="") as csvfile:
            fieldnames = ["date_since", "date_until", "company", "sentiment_score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "date_since": date_since,
                    "date_until": date_until,
                    "company": company,
                    "sentiment_score": mean_sentiment,
                }
            )

    @classmethod
    def get_sentiment(cls, tweet):
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
        cls.classifier.predict(sentence)

        return (
            sentence.labels[0].to_dict()["value"],
            sentence.labels[0].to_dict()["confidence"],
        )

    @classmethod
    def get_activity(cls, company):
        client = tweepy.Client(cls.ELEVATED_KEYS["api_bearer_token"])
        counts = client.get_recent_tweets_count(query=company, granularity="day")
        most_recent_day_count = counts.data[-1]["tweet_count"]
        most_recent_week_count = counts.meta["total_tweet_count"]

        csv_filename = "activity.csv"
        with open(csv_filename, "a", newline="") as csvfile:
            fieldnames = ["company", "week_count", "day_count"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "company": company,
                    "week_count": most_recent_week_count,
                    "day_count": most_recent_day_count,
                }
            )

    @staticmethod
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
        tokenizer = TweetTokenizer(
            preserve_case=False, strip_handles=True, reduce_len=True
        )
        # tokenize tweets
        tweet_tokens = tokenizer.tokenize(result)

        # Import the english stop words list from NLTK
        stopwords_english = stopwords.words("english")

        # Creating a list of words without stopwords
        tweets_clean = []
        for word in tweet_tokens:
            if word not in stopwords_english and word not in string.punctuation:
                tweets_clean.append(word)

        return tweets_clean


if __name__ == "__main__":
    client = TwitterClient()
    # public_tweets = client.get_tweets()
    # print(len(public_tweets))
    # get_sentiment("I am happy")

    # for i in range(2):
    #   print(public_tweets[i].text)
    #   print(clean(public_tweets[i].text))
    #   get_sentiment(public_tweets[i].text)

    search_words = ["#meta", "#stock"]

    date_since_arr = ["202301290000", "202302050000"]
    date_until_arr = ["202302040000", "202302110000"]
    metadata = [True, False]

    # for company in [
    #     "#amc",
    #     "#mullen",
    #     "#microsoft",
    #     "#SPDR",
    #     "#disney",
    #     "#metamaterials",
    #     "#apple",
    #     "#netflix",
    #     "#gamestop",
    #     "#nvidia",
    #     "#amazon",
    #     "#c3ai",
    #     "#bedbathandbeyond",
    #     "#invesco",
    #     "#google",
    #     "#lyft",
    #     "#dteenergy",
    # ]:
    #     client.get_activity(company)

    # Retrieve past tweets in parallel
    # with Pool(5) as p:
    #     p.starmap(
    #         client.get_old_tweets,
    #         zip(
    #             date_since_arr,
    #             date_until_arr,
    #             metadata,
    #             repeat(search_words[0]),
    #             repeat(search_words[1]),
    #         ),
    #     )
