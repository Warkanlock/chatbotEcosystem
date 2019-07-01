"""Install the following requirements:
    dialogflow        0.5.1
    google-api-core   1.4.1
"""

from google.api_core.exceptions import InvalidArgument
import os
import sys
import dialogflow_v2 as dialogflow
import re

CREDENTIALS = './Ecosystem ChatBot-fcb8f6d650b8.json'

class QueryManager():
    def __init__(self):
        self.DIALOGFLOW_PROJECT_ID = 'ecosystem-chatbot'
        self.DIALOGFLOW_LANGUAGE_CODE = 'en-US'
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS
        self.SESSION_ID = 'current-user-id'
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)
        self.response = None

        self.word_keys = {
            'findnumbersection' : self.findnumbersection, # functionName - functionMethod
        }

        print('Session path: {}\n'.format(self.session))
    
    def findnumbersection(self, text_response):
        replace = text_response.replace(r"@number", str(20))
        print(replace)

    def query(self, textQuery):
        text_input = dialogflow.types.TextInput(text=textQuery, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        self.response = self.session_client.detect_intent(session=self.session, query_input=query_input)
        return self.response

    def manageResponse(self, response):
        funcResponse = self.word_keys.get(response.query_result.action.replace(".",""), lambda: "Invalid name")
        funcResponse(response.query_result.fulfillment_text)


test_temp = QueryManager()
response = test_temp.query(sys.argv[1])
test_temp.manageResponse(response)
