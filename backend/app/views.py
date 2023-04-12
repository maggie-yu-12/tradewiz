"""
  Route definitions
"""
import base64
import csv
import itertools
import os
import sys
from datetime import datetime as dt

import aws_controllers.dynamodb.users_controller as users_con
import aws_queries as aws_q
import matplotlib.pyplot as plt
import requests
from flair.data import Sentence
from flair.models import TextClassifier
from flask import Flask, abort, jsonify, render_template, request, send_file
from flask_cors import CORS, cross_origin
from main import app

sys.path.append("app/analysis")
from reddit_client import RedditClient
from twitter_client import TwitterClient

UPLOAD_FOLDER = "/path/to/the/uploads"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

COMPANIES = [
    "#amc",
    "#muln",
    "#googl",
    "#meta",
    "#tsla",
    "#aapl",
    "#nflx",
    "#amzn",
    "#msft",
    "#spy",
    "#dis",
    "#mmat",
    "#gme",
    "#ai",
    "#lyft",
    "#bbby",
    "#qqq",
    "#dte",
]
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
# tclient = TwitterClient()


# example
@app.route("/profile")
@cross_origin(origin="*")
def index():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript",
    }
    return response_body


@app.route("/login", methods=["POST"])
@cross_origin(origin="*")
def get_credentials():
    data = request.get_json()
    print(data)
    email = data["email"]
    password = data["password"]
    res = aws_q.login_user(email, password)
    return res


@app.route("/register", methods=["POST"])
@cross_origin(origin="*")
def register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    username = data["username"]
    res = users_con.register_user(username, password, email)
    return res


@app.route("/weekly_sentiment")
@cross_origin(origin="*")
def get_week():
    res = {}

    for company in COMPANIES:
        last_two_weeks = aws_q.get_two_weeks_sentiment_score_by_company(company)
        last_week = aws_q.get_weekly_sentiment_score_by_company(company)
        sentiment_change = float(last_week) - float(last_two_weeks)
        res[company] = {
            "sentiment_change": {
                "change": round(sentiment_change * 100),
                "prev": round(float(last_two_weeks) * 100, 2),
            },
            "sentiment": round(float(last_week) * 100, 2),
        }

    return res


@app.route("/month_sentiment")
@cross_origin(origin="*")
def get_month():
    res = {}

    for company in COMPANIES:
        last_month = aws_q.get_monthly_sentiment_score_by_company(company)
        res[company] = {
            "sentiment": round(float(last_month) * 100, 2),
        }

    return res


@app.route("/activity")
@cross_origin(origin="*")
def get_activity():
    res = {}
    for company in COMPANIES:
        weekly_activity = aws_q.get_activity_by_company(company)
        res[company] = {
            "weekly_tweets": round(float(weekly_activity) * 100, 2),
        }
    return res


# Retrieves company overview based on stock abbreviation (ex. MSFT)
@app.route("/stockdataoverview", methods=["GET"])
@cross_origin(origin="*")
def get_stock_data_overview():
    stock_abbreviation = request.args.get("symbol")
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_abbreviation}&apikey=1NW9S0JBPSFSTFIL"
    r = requests.get(url)
    response_body_overview = r.json()

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_abbreviation}&apikey=1NW9S0JBPSFSTFIL"
    r = requests.get(url)
    response_body_quote = r.json()

    return {
        "stock_overview": response_body_overview,
        "stock_quote": response_body_quote,
    }


# Retrieves company score based on stock abbreviation (ex. MSFT)
@app.route("/stockdatascore", methods=["GET"])
@cross_origin(origin="*")
def get_stock_data_score():
    stock_abbreviation = request.args.get("symbol")

    twitter_score = float(
        aws_q.get_monthly_sentiment_score_by_company(stock_abbreviation)
    )
    reddit_score = float(rclient.get_sentiment_to_display(stock_abbreviation))
    total_score = (twitter_score + reddit_score) / 2

    return {
        "total_score": round(total_score, 6),
        "twitter_score": round(twitter_score, 6),
        "reddit_score": round(reddit_score, 6),
    }


# Retrieves company activity based on stock abbreviation (ex. MSFT)
@app.route("/stockdataactivity", methods=["GET"])
@cross_origin(origin="*")
def get_stock_data_activity():
    stock_abbreviation = request.args.get("symbol")
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_abbreviation}&apikey=1NW9S0JBPSFSTFIL"
    r = requests.get(url)
    response_body_overview = r.json()

    twitter_activity = float(aws_q.get_activity_by_company(stock_abbreviation))
    reddit_activity = rclient.get_activity(response_body_overview["Name"].split(" ")[0])
    total_activity = twitter_activity + reddit_activity

    return {
        "total_activity": total_activity,
        "twitter_activity": twitter_activity,
        "reddit_activity": reddit_activity,
    }


# Retrieves company news based on stock abbreviation (ex. MSFT)
@app.route("/newsdata", methods=["GET"])
@cross_origin(origin="*")
def get_news_data():
    stock_abbreviation = request.args.get("symbol")

    return {
        "stock_news_twitter": aws_q.get_tweets_by_company(stock_abbreviation),
        "stock_news_reddit": rclient.get_news(stock_abbreviation),
    }


# Retrieves graph based on stock abbreviation
@app.route("/stockgraph", methods=["GET", "POST"])
@cross_origin(origin="*")
def get_stock_graph():
    stock = request.args.get("symbol")
    posts = rclient.get_posts(stock)

    tsla = yf.Ticker(stock)
    tsla_stock = tsla.history(
        start=dt.fromtimestamp(posts["created_at"].min()).strftime("%Y-%m-%d"),
        end=dt.fromtimestamp(posts["created_at"].max()).strftime("%Y-%m-%d"),
        interval="1d",
    ).reset_index()

    # retrieve dates & remove time zone
    date_times = tsla_stock["Date"]
    date_times = [x.tz_convert(None) for x in date_times]

    def getClosestDate(row):
        res = min(date_times, key=lambda sub: abs(sub - row["date"]))
        return res

    # posts["date_group"] = pd.cut(posts["date"], bins=date_bins, labels=date_times)
    # print(posts.head(100))
    posts["date_group"] = posts.apply(getClosestDate, axis=1)

    def getSentiment(row):
        output = rclient.get_sentiment(row["text"])
        return output[0] if output[1] == "POSITIVE" else -1 * output[0]

    posts["sentiment"] = posts.apply(getSentiment, axis=1)
    print(posts.iloc[0])
    df = posts.groupby(["date_group"])["sentiment"].mean()

    print(df.head())

    # plot stock data vs. time
    plt.subplot(1, 2, 1)  # row 1, col 2 index 1
    plt.plot(tsla_stock.Date, tsla_stock.Close)
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.title("Stock Price vs. Time")
    # plot sentiment vs. time
    plt.subplot(1, 2, 2)  # index 2
    plt.plot(df, color="red")
    plt.xlabel("Time")
    plt.ylabel("Avg Sentiment Score")
    plt.title("Avg Sentiment vs. Time")
    filename = stock + "_graph.png"
    plt.savefig(filename)
    img_path = os.path.abspath(filename)
    return jsonify({"image_url": img_path})


@app.route("/time")
@cross_origin(origin="*")
def get_current_time():
    response_body = {
        "time": 2,
    }
    return response_body
