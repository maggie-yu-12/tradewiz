"""
  Route definitions
"""

import csv
import itertools
import os

import requests
from flair.data import Sentence
from flair.models import TextClassifier
from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from main import app

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


# example
@app.route("/profile")
@cross_origin(origin="*")
def index():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript",
    }
    return response_body


# Retrieves company information based on stock abbreviation (ex. MSFT)
@app.route("/stockdata", methods=["GET"])
@cross_origin(origin="*")
def get_stock_data():
    d = dict()
    stock_abbreviation = request.args.get("symbol")
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_abbreviation}&apikey=KZQ08TK5X6QQQDOB"
    r = requests.get(url)
    response_body_overview = r.json()

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_abbreviation}&apikey=KZQ08TK5X6QQQDOB"
    r = requests.get(url)
    response_body_quote = r.json()


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
            sentiment_change = float(row2[3]) - float(row1[3]) / float(row1[3])
            res[row1[2]] = {
                "sentiment_change": round(sentiment_change * 100),
                "sentiment": round(float(row2[3]) * 100),
            }

    return res


@app.route("/month_sentiment")
@cross_origin(origin="*")
def get_month():
    res = {}
    zip_longest = itertools.zip_longest
    with open("app/analysis/prev_week.csv") as prev_file, open(
        "app/analysis/curr_week.csv"
    ) as curr_file:
        prev_reader = csv.reader(prev_file, delimiter=",")
        curr_reader = csv.reader(curr_file, delimiter=",")
        for row1, row2 in zip_longest(prev_reader, curr_reader):
            sentiment_change = float(row2[3]) - float(row1[3]) / float(row1[3])
            res[row1[2]] = {
                "sentiment_change": round(sentiment_change * 100),
                "sentiment": round(float(row2[3]) * 100),
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


# @app.route('/stockname')
# @cross_origin(origin='*')
# def get_name():
#     response_body = {
#         "name": "Microsoft",
#         "about" :"A company based in Redmond, Washington",
#     }
#     return response_body


@app.route("/time")
@cross_origin(origin="*")
def get_current_time():
    response_body = {
        "time": 2,
    }
    return response_body
