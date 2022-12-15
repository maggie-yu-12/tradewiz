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
from datetime import datetime, timedelta
import requests
import pandas as pd

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

  def time_travel(self, now, days):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(days=days)
    return back_in_time.strftime(dtformat)

  def read_config(self):
      """
        Retrieve authentication keys from config file and initialize
      """

      config = configparser.ConfigParser()
      config.read('../../config.ini')

    
      #self.ESSENTIAL_KEYS = {
        #'api_key': config['twitter-essential']['api_key'],
        #'api_key_secret': config['twitter-essential']['api_key_secret'],
        #'api_access_token': config['twitter-essential']['access_token'],
        #'api_access_token_secret': config['twitter-essential']['access_token_secret']
      #}
      
      self.ELEVATED_KEYS = {
        'api_key': config['twitter-elevated']['api_key'],
        'api_key_secret': config['twitter-elevated']['api_key_secret'],
        'api_access_token': config['twitter-elevated']['access_token'],
        'api_access_token_secret': config['twitter-elevated']['access_token_secret']
      }

  def get_tweets(self, since, until):
    """
      API call to get tweets based on query keyword(s)
    """

    query = '(#gme OR gamestop) (lang:en)'
    # try:
    public_tweets = [status for status in tweepy.Cursor(self.api.search_tweets, q=query, result_type='popular', until=until).items(100)]
    return public_tweets
    # except tweepy.TweepError as e:
    #     # print error (if any)
    #     print("Error : " + str(e))


    
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
  #public_tweets = client.get_tweets()
  #print(len(public_tweets))
  # get_sentiment("I am happy")
  dtformat = '%Y-%m-%d'
  now = datetime.now()  # get the current datetime, this is our starting point
  last_week = now - timedelta(days=7)  # datetime one week ago = the finish line
  now = now.strftime(dtformat)  # convert now datetime to format for API
  df = pd.DataFrame()  # initialize dataframe to store tweetS

  tweets = client.get_tweets(now, now)
  for tweet in tweets: 
    row = {
        'id': tweet.id_str,
        'created_at': tweet.created_at,
        'text': tweet.text,
        'sentiment': get_sentiment(tweet.text)
    }
    df.append(row, ignore_index=True)

  print(df)







  #for i in range(2):
    #print(public_tweets[i].text)
    #print(clean(public_tweets[i].text))
    #get_sentiment(public_tweets[i].text)



  # for i in range(2):
  #   print("sentiment score: ", get_sentiment(public_tweets[i]), public_tweets[i])


