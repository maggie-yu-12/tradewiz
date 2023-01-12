"""
  Route definitions
"""

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
@app.route('/profile')
@cross_origin(origin='*') 
def index():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body

# Retrieves company information based on stock abbreviation (ex. MSFT)
@app.route('/stockdata', methods=['POST'])
@cross_origin(origin='*') 
def get_stock_data():
    stock_abbreviation = request.json.get('state')
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_abbreviation}&apikey=KZQ08TK5X6QQQDOB'
    r = requests.get(url)
    response_body = r.json()

    return response_body

@app.route('/time')
@cross_origin(origin='*')
def get_current_time():
    response_body = {
        "time": 2,
    }
    return response_body