"""Install the following requirements:
    dialogflow        0.5.1
    google-api-core   1.4.1
"""

from google.api_core.exceptions import InvalidArgument
import os
import sys
import dialogflow_v2 as dialogflow
import re
import requests
import json

CREDENTIALS = './2513283ecf3d.json'
HOST = 'http://127.0.0.1:5000'


class QueryManager():
    def __init__(self):
        self.DIALOGFLOW_PROJECT_ID = 'ecosystem-chatbot'
        self.DIALOGFLOW_LANGUAGE_CODE = 'en-US'
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS
        self.SESSION_ID = 'current-user-id'
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(
            self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
        self.response = None

        self.word_keys = {
            'findnumbersection': self.findnumbersection,  # functionName - functionMethod
        }

        print('Session path: {}\n'.format(self.session))

    def findnumbersection(self, text_response):
        try:
            response = requests.get(
                HOST + '/graph_api/CountNodes')
            response = response.json()
            replace = text_response.replace(
                r"@number", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace

    def query(self, textQuery):
        text_input = dialogflow.types.TextInput(
            text=textQuery, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        self.response = self.session_client.detect_intent(
            session=self.session, query_input=query_input)
        return self.response

    def manageResponse(self, response):
        funcResponse = self.word_keys.get(
            response.query_result.action.replace(".", ""), lambda: "Invalid name")
        print(funcResponse(response.query_result.fulfillment_text))


test_temp = QueryManager()
response = test_temp.query(sys.argv[1])
test_temp.manageResponse(response)
