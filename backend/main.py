from flask import Flask, make_response, render_template
from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, origins=['*'])
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# def _build_cors_preflight_response():
#     response = make_response()
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "*")
#     response.headers.add("Access-Control-Allow-Methods", "*")
#     return response


# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


from app import views
