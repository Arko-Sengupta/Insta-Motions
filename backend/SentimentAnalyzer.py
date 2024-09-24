import sys
import re
import ast
import logging
import pandas as pd
from typing import Tuple
from scipy.special import softmax
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Encoding for Stdout
sys.stdout.reconfigure(encoding='utf-8')

class TextSentiment:    
    def __init__(self) -> None:
        """
        Initializes the AnalyzeData Class with Instances of SentimentAnalyzer.
        """
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.classifier = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
    def TextClassifier(self, text: str) -> str:
        """
        Classifies the Sentiment of the Text and returns the Sentiment Scores.
        """
        try:
            encoded_text = self.tokenizer(text, return_tensors='pt')
            output = self.classifier(**encoded_text)
            scores = output.logits[0].detach().numpy()
            scores = softmax(scores) 
            return scores
        except Exception as e:
            logging.error("Error in Text Classification: ", exc_info=e)
            raise e
        
class SentimentAnalyzer:
    def __init__(self) -> None:
        """
        Initializes the SentimentAnalyzer Class with an Instance of TextSentiment.
        """
        self.TextAnalyzer = TextSentiment()
        
    def RefineText(self, text: str) -> str:
        """
        Cleans and Refines the Text by Removing Mentions, Hashtags, and Non-Alphanumeric Characters.
        """
        try:
            text = re.sub(r'@', '', text)
            text = re.sub(r'#\w+', '', text)
            text = re.sub(r'[^A-Za-z0-9\s]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        except Exception as e:
            logging.error("Error in Text Refinement: ", exc_info=e)
            raise e
        
    def Analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes Sentiment of Posts and Comments in the DataFrame.
        """
        try:
            df["Post_Text"] = df["Post_Text"].apply(self.RefineText)
            df["Post_Text_Label"] = df["Post_Text"].apply(self.TextAnalyzer.TextClassifier).tolist()
            
            df["Comments"] = df["Comments"].apply(lambda comments: [self.RefineText(comment) for comment in ast.literal_eval(comments)])
            df["Comments_Label"] = df["Comments"].apply(lambda comments: {comment: self.TextAnalyzer.TextClassifier(comment).tolist() for comment in comments})
            
            return df
        except Exception as e:
            logging.error("Error in Sentiment Analysis: ", exc_info=e)
            raise e
        
class AnalyzeData:
    def __init__(self) -> None:
        """
        Initializes the FetchData Class with Instances of SentimentAnalyzer.
        """
        self.sentiment_analyzer = SentimentAnalyzer()
        
    def run(self, data: dict) -> Tuple[pd.DataFrame, bool]:
        """
        Analyze Sentiments of Posts & Comments from Instagram
        """
        try:
            df = pd.DataFrame(data)
            df = self.sentiment_analyzer.Analyze(df)
            
            return df, True
        except Exception as e:
            logging.error("Error in Fetching Data: ", exc_info=e)
            return pd.DataFrame(), False