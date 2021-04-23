"""
Pierre-Charles Dussault
October 28, 2020

A class modeling a single-question survey. Its purpose is to test unit testing
features in Python.
"""

class AnonymousSurvey():
    """Collect anonymous answers to a survey question."""

    def __init__(self, question):
        """Store a question, then prepare to store responses."""
        self.question = question
        self.responses = []

    def show_question(self):
        """Display the question"""
        print(self.question)

    def store_response(self, new_response):
        """Store a new response."""
        self.responses.append(str(new_response).title())

    def show_results(self):
        """Display all the responses that have been given."""
        print("Survey results: ")
        for each_response in self.responses:
            print ('- ' + each_response)
