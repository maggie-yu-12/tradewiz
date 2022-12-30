"""

Referenced tutorials to set up authentication here: 
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac
  > https://medium.com/mlearning-ai/how-to-get-tweets-by-python-and-twitter-api-2022-a440c635c3ac

"""

import configparser
import tweepy
from flair.models import TextClassifier
from flair.data import Sentence
from flair.models import SequenceTagger
import re
import requests
import json



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
    auth = tweepy.OAuthHandler(self.ELEVATED_KEYS['api_key'], self.ELEVATED_KEYS['api_key_secret'])
    auth.set_access_token(self.ELEVATED_KEYS['api_access_token'], self.ELEVATED_KEYS['api_access_token_secret'])
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

  def read_config(self):
      """
        Retrieve authentication keys from config file and initialize
      """

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

  def get_tweets(self):
    """
      API call to get tweets based on query keyword(s)
    """

    query = '#gme'

    # try:
    public_tweets = [status for status in tweepy.Cursor(self.api.search_tweets, q=query).items(100)]
    return public_tweets
    # except tweepy.TweepError as e:
    #     # print error (if any)
    #     print("Error : " + str(e))

  def get_old_tweets(self):
    endpoint = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"


    headers = {"Authorization":{self.ESSENTIAL_KEYS['api_bearer_token']}, "Content-Type": "application/json"}

    data = '{"query":"(snow OR sleet OR hail OR (freezing rain)) has:images", "fromDate": "201802020000", "toDate": "201802240000"}'

    response = requests.post(endpoint,data=data,headers=headers).json()

    print(json.dumps(response, indent = 2))


'''
  For a tweet, return get sentiment score through Flair API
  Input: tweet str
  Return: score float
'''
def get_sentiment(tweet):
  # > Referenced: https://towardsdatascience.com/text-classification-with-state-of-the-art-nlp-library-flair-b541d7add21f?gi=3675966b8dff
  classifier = TextClassifier.load('en-sentiment')
  sentence = Sentence(tweet)
  classifier.predict(sentence)
  # print('Sentence above is: ', sentence.labels)
  print(tweet)
  print(sentence.labels[0].to_dict()['value'])
  print(sentence.labels[0].to_dict()['confidence'])
  
  # stacked_embeddings.embed(text)
  # classifier.predict(text)
  # value = text.labels[0].to_dict()['value'] 
  # if value == 'POSITIVE':
  #     result = text.to_dict()['labels'][0]['confidence']
  # else:
  #     result = -(text.to_dict()['labels'][0]['confidence'])
      
  # return round(result, 3)
  
def clean(raw):
    """ Remove hyperlinks and markup """
    result = re.sub("<[a][^>]*>(.+?)</[a]>", 'Link.', raw)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    return result
    
if __name__ == '__main__':
  client = TwitterClient()
  public_tweets = client.get_tweets()
  print(len(public_tweets))
  # get_sentiment("I am happy")

  # for i in range(2):
  #   print(public_tweets[i].text)
  #   print(clean(public_tweets[i].text))
  #   get_sentiment(public_tweets[i].text)

  client.get_old_tweets()

  # for i in range(2):
  #   print("sentiment score: ", get_sentiment(public_tweets[i]), public_tweets[i])


