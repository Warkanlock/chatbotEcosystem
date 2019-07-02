import requests

HOST = 'http://127.0.0.1:5000'


class AnswerManager():
    def __init__(self):
        self.answer = None

        self.word_keys = {
            'inputwelcome': self.hi,
            'findnumbersection': self.findnumbersection,  # functionName - functionMethod
            'findrelatedofferings': self.findrelatedofferings,
            'findrelatedsections': self.findrelatedsections,
        }

    def hi(self, text_response):
        return text_response

    def findnumbersection(self, text_response, parameters=None):
        try:
            response = requests.get(HOST + '/graph_api/CountNodes')
            response = response.json()
            print(response)
            replace = text_response.replace(r"@number", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace

    def findrelatedofferings(self, text_response, parameters):
        try:
            title = parameters.fields['any'].string_value
            response = requests.get(
                HOST + '/graph_api/RelatedOffering/' + str(title))  # check this query
            response = response.json()
            replace = text_response.replace(r"@offerings", str(response[0][0]))
        except ReferenceError as e:
            return -1
        return replace

    def findrelatedsections(self, text_response, parameters):
        try:
            response = requests.get(
                HOST + '/graph_api/RelatedNode?sec='+parameters.fields['any'].string_value)  # check this query
            response = response.json()
            numberSectionRelated = []
            for element in response:
                numberSectionRelated.append(element['sectionRelated'])

            appendSections = ', '.join(numberSectionRelated)
            replace = text_response.replace(
                r"@sections", appendSections)
        except ReferenceError as e:
            return -1
        return replace

    def chooseAnswer(self, response):
        method_name = self.word_keys.get(
            response.query_result.action.replace(".", ""), "Invalid name")

        if method_name == "Invalid name":
            return "Invalid Question"
        parameters = response.query_result.parameters
        if parameters:
            return method_name(text_response=response.query_result.fulfillment_text,
                               parameters=response.query_result.parameters)
        else:
            return method_name(text_response=response.query_result.fulfillment_text)
