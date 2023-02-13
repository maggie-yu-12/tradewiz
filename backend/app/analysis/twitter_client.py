"""
Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
"""


import configparser
import json
import re
import string
from itertools import repeat
from multiprocessing import Pool

import flair as flair
import nltk
import requests
import tweepy
import yfinance as yf
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
        # TwitterClient.setup_config()
        self.setup_config()

        ### ESSENTIAL ACCESS VERSION ###
        # self.client = tweepy.Client(
        # consumer_key=API_KEY,
        # consumer_secret=API_KEY_SECRET,
        # access_token=ACCESS_TOKEN,
        # access_token_secret=ACCESS_TOKEN_SECRET)

        # except tweepy.TweepError as e:
        #   # print error (if any)
        #   print("Error : " + str(e))

    # @classmethod
    def read_config(self):
        """
        Retrieve authentication keys from config file and initialize
        """

        config = configparser.RawConfigParser()
        config.read("../../config.ini")

        # self.ESSENTIAL_KEYS = {
        #'api_key': config['twitter-essential']['api_key'],
        #'api_key_secret': config['twitter-essential']['api_key_secret'],
        #'api_access_token': config['twitter-essential']['access_token'],
        #'api_access_token_secret': config['twitter-essential']['access_token_secret'],
        #'api_bearer_token': config['twitter-essential']['bearer_token'],
        # }

        self.ELEVATED_KEYS = {
            "api_key": config["twitter-elevated"]["api_key"],
            "api_key_secret": config["twitter-elevated"]["api_key_secret"],
            "api_access_token": config["twitter-elevated"]["access_token"],
            "api_access_token_secret": config["twitter-elevated"][
                "access_token_secret"
            ],
            "api_bearer_token": config["twitter-elevated"]["bearer_token"],
        }

        # self.BEARER_TOKEN = config['twitter-essential']['bearer_token']

    # @classmethod
    def setup_config(self):
        """
        Set up authentication and initialize client
        """

        self.read_config()

        ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
        auth = tweepy.OAuthHandler(
            self.ESSENTIAL_KEYS["api_key"], self.ESSENTIAL_KEYS["api_key_secret"]
        )
        auth.set_access_token(
            self.ESSENTIAL_KEYS["api_access_token"],
            self.ESSENTIAL_KEYS["api_access_token_secret"],
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    # @classmethod
    def get_old_tweets(self, date_since, date_until, *search_words):
        """
        Queries past tweets based on provided query and date range and writes them to local files based on date range
        Args:
            date_since (string): Start date from which we want to query the tweets from
            date_until (string): End date to which we want to query the tweets until
            *search_words: Variable argumens for search words (multiple search words are OR'ed by default)
        Returns: None
        """
        # Create a name for file that we will be writing tweets to
        filename = "past_tweets_" + date_since + "_" + date_until + ".txt"
        search_string = " OR ".join(search_words)

        # UNCOMMENT TO RUN THE QUERIES
        # !! NOTE: WE NEED TO BE CAREFUL BC WE CAN run AT MAX 50 QUERIES PER MONTH :((
        tweets = tweepy.Cursor(
            self.api.search_full_archive,
            query=search_string,
            label="fullArchiveEnviron",
            fromDate=date_since,
            toDate=date_until,
        ).items(limit=10)

        with open(filename, "w") as file:
            for elem in tweets:
                # Turn Status (`elem` data type) object into a JSON format to make writable to a file
                s = json.dumps(elem._json)
                file.write(s)
        #        file.write("\n")

    # @classmethod
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
        sentiment_model = flair.models.TextClassifier.load("en-sentiment")
        x = sentiment_model.predict(sentence)

        return sentence.labels

        # stacked_embeddings.embed(text)
        # classifier.predict(text)
        # value = text.labels[0].to_dict()['value']
        # if value == 'POSITIVE':
        #     result = text.to_dict()['labels'][0]['confidence']
        # else:
        #     result = -(text.to_dict()['labels'][0]['confidence'])

        # return round(result, 3)

    # @staticmethod
    def clean(self, tweet_text):
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
    # client.read_config()
    # client.setup_config()
    # public_tweets = client.get_tweets()
    # print(len(public_tweets))
    # get_sentiment("I am happy")

    # for i in range(2):
    #   print(public_tweets[i].text)
    #   print(clean(public_tweets[i].text))
    #   get_sentiment(public_tweets[i].text)

    search_words = ["#tesla", "#stock"]

    date_since_arr = ["201610310000", "201611050000"]
    date_until_arr = ["201611020000", "201611060000"]
    # client.get_old_tweets(date_since_arr[0], date_until_arr[0], search_words[0])

    # Retrieve past tweets in parallel
    # with Pool(5) as p:
    # p.starmap(client.get_old_tweets, zip(
    # date_since_arr, date_until_arr, repeat(search_words[0]), repeat(search_words[1])))

    client.get_old_tweets(date_since_arr[0], date_until_arr[0], search_words[0])

    # Reads in files with past tweets and extracts out text from each
    queried_tweets = []

    with open("past_tweets_201610310000_201611020000.txt", "r") as file:
        for line in file:
            obj = json.loads(line)
            queried_tweets.append(obj["text"])

    sentiments = []
    for tweet in queried_tweets:
        sentiments.append(client.get_sentiment(client.clean(tweet)))

    print(sentiments)

    tsla = yf.Ticker("TSLA")
    tsla_stock = tsla.history(
        start=(date_since_arr[0].strftime("%Y-%m-%d")),
        end=date_until_arr[0].strftime("%Y-%m-%d"),
        interval="60m",
    ).reset_index()
