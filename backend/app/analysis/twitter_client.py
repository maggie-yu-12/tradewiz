"""

Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac

"""

# pylint: disable=E1136

import configparser
import json
import re
import requests
from client import Client

import tweepy
from flair.data import Sentence
from flair.models import SequenceTagger, TextClassifier


'''
    Twitter client class for sentiment analysis
'''
class TwitterClient(Client):

    '''
        Set up authentication and initialize client
    '''
    def __init__(self):
        self.read_config()

        ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
        auth = tweepy.OAuthHandler(
            self.ELEVATED_KEYS['api_key'], self.ELEVATED_KEYS['api_key_secret'])
        auth.set_access_token(
            self.ELEVATED_KEYS['api_access_token'], self.ELEVATED_KEYS['api_access_token_secret'])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        ### ESSENTIAL ACCESS VERSION ###
        # self.client = tweepy.Client(
        # consumer_key=API_KEY,
        # consumer_secret=API_KEY_SECRET,
        # access_token=ACCESS_TOKEN,
        # access_token_secret=ACCESS_TOKEN_SECRET)

        # except tweepy.TweepError as e:
        #   # print error (if any)
        #   print("Error : " + str(e))

    
    """
        Retrieve authentication keys from config file and initialize
    """
    def read_config(self):
        config = configparser.ConfigParser()
        config.read('../../config.ini')

        self.ESSENTIAL_KEYS = {
            'api_key': config['twitter-essential']['api_key'],
            'api_key_secret': config['twitter-essential']['api_key_secret'],
            'api_access_token': config['twitter-essential']['access_token'],
            'api_access_token_secret': config['twitter-essential']['access_token_secret'],
            'api_bearer_token': config['twitter-essential']['bearer_token'],
        }

        self.ELEVATED_KEYS = {
            'api_key': config['twitter-elevated']['api_key'],
            'api_key_secret': config['twitter-elevated']['api_key_secret'],
            'api_access_token': config['twitter-elevated']['access_token'],
            'api_access_token_secret': config['twitter-elevated']['access_token_secret']
        }

        # self.BEARER_TOKEN = config['twitter-essential']['bearer_token']
    """
        API call to get tweets based on query keyword(s)
    """
    def get_posts(self):
        query = '#gme' # TODO: change to take in query keyword

        # try:
        public_tweets = [status for status in tweepy.Cursor(
            self.api.search_tweets, q=query).items(100)]
        return public_tweets
        # except tweepy.TweepError as e:
        #     # print error (if any)
        #     print("Error : " + str(e))

    def get_old_tweets(self):
        endpoint = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"

        headers = {"Authorization": {
            self.ESSENTIAL_KEYS['api_bearer_token']}, "Content-Type": "application/json"}

        data = '{"query":"(snow OR sleet OR hail OR (freezing rain)) has:images", "fromDate": "201802020000", "toDate": "201802240000"}'

        response = requests.post(endpoint, data=data, headers=headers).json()

        print(json.dumps(response, indent=2))


if __name__ == '__main__':
    client = TwitterClient()
    public_tweets = client.get_posts()
    print(len(public_tweets))
    # get_sentiment("I am happy")

    # for i in range(2):
    #   print(public_tweets[i].text)
    #   print(clean(public_tweets[i].text))
    #   get_sentiment(public_tweets[i].text)

    client.get_old_tweets()

    for i in range(2):
      print("sentiment score: ", client.get_sentiment(public_tweets[i]), public_tweets[i])
