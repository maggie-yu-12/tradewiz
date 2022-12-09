import flair
import pandas as pd

sentiment_model = flair.models.TextClassifier.load('en-sentiment')

params = {
    'q': 'tesla',
    'tweet_mode': 'extended',
    'lang': 'en',
    'count': '100'
}

requests.get(
    'https://api.twitter.com/1.1/search/tweets.json?q=tesla',
    params=params,
    headers={
        'authorization': 'Bearer '+AAAAAAAAAAAAAAAAAAAAAGJTjQEAAAAAFVA2HcOK%2FcR%2Fc2FPcKcfGdCvos8%3DqJ0x4Lafh439mFUHO9Sgez6Q2iFou3B1IqEvCNBSEGnEwz87DR

})

def get_data(tweet):
    data = {
        'id': tweet['id_str'],
        'created_at': tweet['created_at'],
        'text': tweet['full_text']
    }
    return data


df = pd.DataFrame()

for tweet in response.json()['statuses']:
    row = get_data(tweet)
    df = df.append(row, ignore_index=True)

sentence = flair.data.Sentence(TEXT)
sentiment_model.predict(sentence)


