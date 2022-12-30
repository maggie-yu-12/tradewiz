"""
  Route definitions
"""

from main import app

from flask_cors import cross_origin

from flask import abort, Flask, jsonify, request
from flair.models import TextClassifier
from flair.data import Sentence

import requests, os
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

