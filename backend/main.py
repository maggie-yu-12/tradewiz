
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/profile')
def index():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

    # return render_template('index.html')