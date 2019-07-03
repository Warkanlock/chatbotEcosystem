from chatbot import query
from chatbot import answers
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates')

test_temp = query.QueryManager()


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
