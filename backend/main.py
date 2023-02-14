from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, origins=['*'])
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

from app import views
