"""

Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac

"""

import configparser
import tweepy

# Retrieve authentication keys from config file
def read_config():
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

# Setup access to API
def connect_to_twitter_OAuth():
    read_config()

    ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
    # auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # api = tweepy.API(auth)
    # return api

    client = tweepy.Client(
      consumer_key=API_KEY,
      consumer_secret=API_KEY_SECRET,
      access_token=ACCESS_TOKEN,
      access_token_secret=ACCESS_TOKEN_SECRET)
      
    return client

if __name__ == '__main__':
  ### ONLY AVAILABLE FOR ELEVATED ACCESS ###
  # Create API object
  # api = connect_to_twitter_OAuth()
  # public_tweets = api.home_timeline()
  # print(public_tweets)

  ### ESSENTIAL ACCESS VERSION ###
  client = connect_to_twitter_OAuth()
  query = 'news'
  tweets = client.search_recent_tweets(query=query, max_results=10, user_auth=True)
  for tweet in tweets.data:
    print(tweet.text)
