"""
  Route definitions
"""

import csv
import itertools
import os
import sys

import requests
from flair.data import Sentence
from flair.models import TextClassifier
from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from main import app

sys.path.append("app/analysis")
from reddit_client import RedditClient

# session = requests.Session()
# session.verify = False
# session.trust_env = False
# os.environ['CURL_CA_BUNDLE']=""


# @app.route('/api/v1/analyzeSentiment', methods=['POST'])
# def analyzeSentiment():
# classifier = TextClassifier.load('sentiment')
# if not request.json or not 'message' in request.json:
#     abort(400)
# message = request.json['message']
# sentence = Sentence(message)
# classifier.predict(sentence)
# print('Sentence sentiment: ', sentence.labels)
# label = sentence.labels[0]
# response = {'result': label.value, 'polarity':label.score}
# return jsonify(response), 200

rclient = RedditClient()


# example
@app.route("/profile")
@cross_origin(origin="*")
def index():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript",
    }
    return response_body


@app.route("/weekly_sentiment")
@cross_origin(origin="*")
def get_week():
    res = {}
    zip_longest = itertools.zip_longest
    with open("app/analysis/prev_week.csv") as prev_file, open(
        "app/analysis/curr_week.csv"
    ) as curr_file:
        prev_reader = csv.reader(prev_file, delimiter=",")
        curr_reader = csv.reader(curr_file, delimiter=",")
        for row1, row2 in zip_longest(prev_reader, curr_reader):
            num2 = float(row2[3])
            num1 = float(row1[3])
            sentiment_change = (num2 - num1) / num1
            print(sentiment_change)
            res[row1[2]] = {
                "sentiment_change": {
                    "change": round(sentiment_change * 100),
                    "prev": round(float(row1[3]) * 100, 2),
                },
                "sentiment": round(float(row2[3]) * 100, 2),
            }

    return res


@app.route("/month_sentiment")
@cross_origin(origin="*")
def get_month():
    res = {}
    with open("app/analysis/prev_month.csv") as curr_file:
        curr_reader = csv.reader(curr_file, delimiter=",")
        for row1 in curr_reader:
            res[row1[2]] = {
                "sentiment": round(float(row1[3]) * 100, 2),
            }

    return res


@app.route("/activity")
@cross_origin(origin="*")
def get_activity():
    res = {}
    with open("app/analysis/activity.csv") as csv_file:
        prev_reader = csv.reader(csv_file, delimiter=",")
        for row in prev_reader:
            res[row[0]] = {"week_tweets": float(row[1]), "day_tweets": float(row[2])}
    return res


# Retrieves company information based on stock abbreviation (ex. MSFT)
@app.route("/stockdata", methods=["GET"])
@cross_origin(origin="*")
def get_stock_data():
    d = dict()
    stock_abbreviation = request.args.get("symbol")
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_abbreviation}&apikey=1NW9S0JBPSFSTFIL"
    r = requests.get(url)
    response_body_overview = r.json()

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_abbreviation}&apikey=1NW9S0JBPSFSTFIL"
    r = requests.get(url)
    response_body_quote = r.json()

    print(rclient.get_posts(stock_abbreviation))

    return {
        "stock_overview": response_body_overview,
        "stock_quote": response_body_quote,
        "stock_news": rclient.get_posts(stock_abbreviation),
    }


@app.route("/time")
@cross_origin(origin="*")
def get_current_time():
    response_body = {
        "time": 2,
    }
    return response_body
