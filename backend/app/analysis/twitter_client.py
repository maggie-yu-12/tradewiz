"""

Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac

"""

import configparser
import tweepy

class TwitterClient(object):
  """
    Twitter client class for sentiment analysis
  """

  def __init__(self):
    """
      Set up authentication and initialize client
    """
    self.read_config()

    ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
    # auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # api = tweepy.API(auth)
    # return api

    try: 
      self.client = tweepy.Client(
      consumer_key=API_KEY,
      consumer_secret=API_KEY_SECRET,
      access_token=ACCESS_TOKEN,
      access_token_secret=ACCESS_TOKEN_SECRET)

    except tweepy.TweepError as e:
      # print error (if any)
      print("Error : " + str(e))

  def read_config(self):
      """
        Retrieve authentication keys from config file and initialize
      """

      config = configparser.ConfigParser()
      config.read('../config.ini')

      global API_KEY
      global API_KEY_SECRET
      global ACCESS_TOKEN
      global ACCESS_TOKEN_SECRET
      
      API_KEY = config['twitter']['api_key']
      API_KEY_SECRET = config['twitter']['api_key_secret']

      ACCESS_TOKEN = config['twitter']['access_token']
      ACCESS_TOKEN_SECRET = config['twitter']['access_token_secret']

  def get_tweets(self):
    """
      API call to get tweets based on query keyword(s)
    """

    query = 'Elon Musk'

    try:
      tweets = self.client.search_recent_tweets(query=query, max_results=10, user_auth=True)
      print(tweets)
      for tweet in tweets:
        print(tweet)
    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))

if __name__ == '__main__':
  ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
  # Create API object
  # api = connect_to_twitter_OAuth()
  # public_tweets = api.home_timeline()
  # print(public_tweets)

  ### ESSENTIAL ACCESS VERSION ###
  client = TwitterClient()
  client.get_tweets()
