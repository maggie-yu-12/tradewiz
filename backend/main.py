
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins=[
  'http://localhost:1234',
])
app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

from app import views