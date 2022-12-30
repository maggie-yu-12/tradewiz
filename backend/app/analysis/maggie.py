# # twitter API
# import os

# import tweepy as tw
# # Imports the Google Cloud client library
# from google.cloud import language_v1

# # Instantiates a client
# client = language_v1.LanguageServiceClient()

# # Twitter API Authentication Steps

# # analyzes the tweet's content and returns a float from -1 to 1 (sentiment score)


# def get_sentiment_score(text):
#     document = language_v1.Document(
#         content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

#     # Detects the sentiment of the text
#     sentiment = client.analyze_sentiment(
#         request={'document': document}).document_sentiment

#     # print("Text: {}".format(text))
#     # print("Sentiment: " + str(sentiment.score))
#     return sentiment.score


# '''
#     main function to be called. Returns two lists pos and neg with the top 5 positive and negative tweets and its properties.
#     input should be ABC, not #ABC or $ABC. The search uses the $ filter only.
#     input: stock_name str
#     return: sentiment_score float
# '''


# def get_twitter_top_tweets_(stock_name):
#     search_words = "$" + stock_name + " -filter:retweets"
#     date_since = "2022-11-01"
#     tweets = tw.Cursor(api.search,
#                        q=search_words,
#                        tweet_mode='extended',
#                        result_type='popular',
#                        lang="en",
#                        since=date_since
#                        ).items()

#     tweets_arr = []
#     month = ""
#     day = ""
#     hour = 0
#     minute = ""
#     ampm = ""

#     for tweet in tweets:
#         # month
#         if tweet.created_at.month == 11:
#             month = "November"
#         else:
#             month = "December"

#         # day
#         day = tweet.created_at.day

#         # time
#         if tweet.created_at.hour == 0:
#             ampm = "AM"
#             hour = 12
#         elif tweet.created_at.hour > 12:
#             ampm = "PM"
#             hour = tweet.created_at.hour - 12
#         else:
#             ampm = "AM"
#             hour = tweet.created_at.hour
#         if tweet.created_at.minute < 10:
#             minute = "0" + str(tweet.created_at.minute)
#         else:
#             minute = str(tweet.created_at.minute)

#         date = str(month) + " " + str(day) + ", 2021 @ " + \
#             str(hour) + ":" + str(minute) + " " + ampm

#         tweets_arr.append([tweet.user.name, tweet.user.screen_name, date, tweet.full_text, tweet.retweet_count,
#                            tweet.favorite_count, tweet.user.profile_image_url_https, get_sentiment_score(tweet.full_text)])

#     if len(tweets_arr) > 50:
#         # sort by number of likes to get top 50 tweets on the stock
#         tweets_arr.sort(key=lambda x: x[5], reverse=True)
#         tweets_arr = tweets_arr[:51]

#     tweets_arr.sort(key=lambda x: x[-1])

#     neg = []
#     pos = []
#     neut = []
#     neg_counter = 0
#     pos_counter = -1
#     neut_start = -1
#     neut_end = -1
#     for i in range(len(tweets_arr)):
#         if tweets_arr[i][-1] > - 0.3 and tweets_arr[i][-1] < 0.3:
#             neut_start = i
#             break
#     for j in range(len(tweets_arr) - 1, -1, -1):
#         if tweets_arr[j][-1] > - 0.3 and tweets_arr[j][-1] < 0.3:
#             neut_end = i
#             break

#     if len(tweets_arr) > 0:
#         while neg_counter < 5 and tweets_arr[neg_counter][-1] < -0.3:
#             neg.append(tweets_arr[neg_counter][0:7])
#             neg_counter += 1
#         while pos_counter > -6 and tweets_arr[pos_counter][-1] > 0.3:
#             pos.append(tweets_arr[pos_counter][0:7])
#             pos_counter -= 1
#         if neut_start != -1 and neut_end != -1 and neut_start <= neut_end:
#             mid = int(neut_start + (neut_end - neut_start) / 2)
#             neut.append(tweets_arr[mid][0:7])
#             l = mid - 1
#             r = mid + 1
#             left_valid = True
#             right_valid = True
#             while (left_valid or right_valid) and len(neut) < 5:
#                 if l >= 0 and tweets_arr[l][-1] > -0.3:
#                     neut.append(tweets_arr[l][0:7])
#                     l -= 1
#                 else:
#                     left_valid = False
#                 if r < len(tweets_arr) and tweets_arr[r][-1] < 0.3:
#                     neut.append(tweets_arr[r][0:7])
#                     r += 1
#                 else:
#                     right_valid = False

#     return pos, neg, neut


# pos, neg, neut = get_twitter_top_tweets_("TSLA")

# print(pos)
# print(neg)
