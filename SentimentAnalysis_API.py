import os
import sys
import logging
import pandas as pd
from flask import Blueprint, Flask, jsonify, request
from backend.SentimentAnalyzer import AnalyzeData

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Append Parent Directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class SentimentAnalyze:
    def __init__(self):
        """Initializes the SentimentAnalyze Class."""
        self.analyzer = AnalyzeData()

    def run(self, username: str, password: str) -> str:
        """Runs Sentiment Analysis on the provided Credentials."""
        try:
            return self.analyzer.run(username, password)
        except Exception as e:
            logging.error('An Error Occurred during Analysis', exc_info=e)
            raise

class SentimentAnalyzeAPI:
    """API Class that sets up Flask Application with routes for SentimentAnalyze Interaction."""
    
    def __init__(self):
        """Initializes the Flask App and sets up routes."""
        self.app = Flask(__name__)
        self.sentimentanalyze_blueprint = Blueprint('sentimentanalyze', __name__)
        self.sentimentanalyze_blueprint.add_url_rule('/Posts', 'Posts', self.Sentiment_Analyze, methods=['POST'])
        self.sentimentanalyze = SentimentAnalyze()

    def Sentiment_Analyze(self) -> tuple:
        """Handles the /posts URL, processes the Input Credentials, and returns the response."""
        try:
            credentials = request.get_json()
            username = credentials.get("username")
            password = credentials.get("password")
            
            response = list(self.sentimentanalyze.run(username, password))
            response[0] = response[0].to_dict(orient='records')
            
            return jsonify({'response': response}), 200
        except Exception as e:
            logging.error('An Error Occurred while Handling the Request', exc_info=e)
            return jsonify({'Error': str(e)}), 400

    def run(self) -> None:
        """Starts the Flask Application with the registered blueprint."""
        try:
            self.app.register_blueprint(self.sentimentanalyze_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An Error Occurred while Starting the Server', exc_info=e)
            raise

if __name__ == '__main__':
    
    server = SentimentAnalyzeAPI()
    server.run()