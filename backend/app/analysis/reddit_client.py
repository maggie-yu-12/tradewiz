import configparser
import json
import re
from client import Client

import praw
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

        # Read-only instance
        self.reddit_read_only = praw.Reddit(client_id="jR-4thKK9gWzUeWbmoMnXQ", client_secret="5N8JI3jtN0Jn56CrXpLfkLBDulnCeQ", user_agent="retrieve_wallstreetbets_content")
        
        # self.subreddit = reddit_read_only.subreddit("wallstreetbets")
        
        # print("Display Name:", self.subreddit.display_name)
 
        # Display the title of the Subreddit
        # print("Title:", self.subreddit.title)

    '''
      API call to get tweets based on query keyword(s)
    '''
    def get_posts(self):
      query = "GME"
      response = []
      for submission in self.reddit_read_only.subreddit("all").search(query, sort='top', time_filter='week'):
        print(submission.selftext)
        response.append(submission.title + submission.selftext)
      
      return response

if __name__ == '__main__':
    client = RedditClient()
    posts = client.get_posts()
    for i in range(2):
      print("sentiment score: ", client.get_sentiment(posts[i]), posts[i])


    
