from chatbot import query
from chatbot import answers
from flask import Flask

app = Flask(__name__)

test_temp = query.QueryManager()


@app.route('/index')
def index():
    response = test_temp.query('How many sections are?')
    hello = test_temp.manageResponse(response)
    return hello
