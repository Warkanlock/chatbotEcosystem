from chatbot import query
from chatbot import answers
from flask import Flask, render_template, request, jsonify
import requests

# soy fede

app = Flask(__name__, template_folder='./templates')

test_temp = query.QueryManager()
HOST = 'http://127.0.0.1:5000'


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', text='Just ask me anything about US CODE...')
    if request.method == 'POST':
        question = request.form
        response = test_temp.query(question['question'])
        text = test_temp.manageResponse(response)
        return text


def findnumbersection(text_response):
    try:
        response = requests.get(HOST + '/graph_api/CountNodes')
        response = response.json()
        print(response)
        replace = text_response.replace(r"@number", str(response[0][0]))
    except ReferenceError as e:
        return -1
    return replace


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json(silent=True)
    if data['queryResult']['action'] == 'input.welcome':
        reply = {
            "fulfillmentText": "Hi, I'm Chatboy.  [ PwC Proof of Concept ]",
        }
    elif data['queryResult']['action'] == 'find.number.section':
        responseText = findnumbersection(
            data['queryResult']['fulfillmentMessages'][0]['text']['text'][0])
        reply = {
            "fulfillmentText": responseText
        }
    return jsonify(reply)
