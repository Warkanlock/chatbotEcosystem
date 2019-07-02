import requests

HOST = 'http://127.0.0.1:5000'

class AnswerManager():
    def __init__(self):
        self.answer = None

        self.word_keys = {
            'findnumbersection': self.findnumbersection,  # functionName - functionMethod
            'findrelatedofferings' : self.findrelatedofferings,
            'findranddofferings' : self.findranddofferings,
        }

    def findnumbersection(self, text_response, parameters=None):
        try:
            response = requests.get(HOST + '/graph_api/CountNodes')
            response = response.json()
            replace = text_response.replace(r"@number", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace
    
    def findrelatedofferings(self, text_response, parameters):
        try:
            title = parameters.fields['any'].string_value
            response = requests.get(HOST + '/graph_api/RelatedOffering/' + str(title)) ### check this query
            response = response.json()
            replace = text_response.replace(r"@offerings", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace

    def findranddofferings(self, text_response, parameters=None):
        try:
            response = requests.get(HOST + '/graph_api/RelatedOffering') ### check this query
            response = response.json()
            replace = text_response.replace(r"@rdofferings", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace
        
    def chooseAnswer(self, response):
        method_name = self.word_keys.get(response.query_result.action.replace(".", ""), lambda: "Invalid name")
        if method_name == "Invalid name":
            print("Invalid Question")
            return -1
        return method_name(text_response=response.query_result.fulfillment_text, parameters=response.query_result.parameters))
