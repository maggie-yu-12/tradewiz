import re

from flair.data import Sentence
from flair.models import SequenceTagger, TextClassifier


class Client:
  def __init__(self):
    pass

  def get_posts(self, query):
    pass

  '''
    Remove hyperlinks and markup
  '''
  def clean(self, raw):
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

  '''
  For a tweet, return get sentiment score through Flair API
  Input: tweet str
  Return: score float
  '''
  def get_sentiment(self, post):
    # > Referenced: https://towardsdatascience.com/text-classification-with-state-of-the-art-nlp-library-flair-b541d7add21f?gi=3675966b8dff
    classifier = TextClassifier.load('en-sentiment')
    post = self.clean(post)
    sentence = Sentence(post)
    classifier.predict(sentence)
    print(post)
    print(sentence.labels[0].to_dict()['value'])
    print(sentence.labels[0].to_dict()['confidence'])
