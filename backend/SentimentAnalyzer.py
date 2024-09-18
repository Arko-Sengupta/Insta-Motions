import re
import sys
import logging
import instaloader
import pandas as pd
from scipy.special import softmax
from typing import Tuple, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Encoding for Stdout
sys.stdout.reconfigure(encoding='utf-8')

class TextSentiment:    
    def __init__(self) -> None:
        """
        Initializes the TextSentiment Class
        """
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.classifier = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
    def TextClassifier(self, text: str) -> str:
        """
        Classifies the Sentiment of the Text.
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
            df["Post_Text_Label"] = df["Post_Text"].apply(self.TextAnalyzer.TextClassifier)
            
            df["Comments"] = df["Comments"].apply(lambda comments: [self.RefineText(comment) for comment in comments])
            df["Comments_Label"] = df["Comments"].apply(lambda comments: {comment: self.TextAnalyzer.TextClassifier(comment) for comment in comments})
            
            return df
        except Exception as e:
            logging.error("Error in Sentiment Analysis: ", exc_info=e)
            raise e
        
class AnalyzeData:
    def __init__(self) -> None:
        """
        Initializes the FetchData Class with Instances of SentimentAnalyzer and Instaloader.
        """
        self.sentiment_analyzer = SentimentAnalyzer()
        self.instaloader = instaloader.Instaloader()
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        
    def AuthCredential(self) -> bool:
        """
        Authenticates the Instagram Credentials.
        """
        try:
            if self.username and self.password:
                self.instaloader.login(self.username, self.password)
                return True
            else:
                logging.warning("Username or Password not Set.")
                return False
        except Exception as e:
            logging.error("Error in Authentication: ", exc_info=e)
            return False
        
    def run(self, username: str, password: str) -> Tuple[pd.DataFrame, bool]:
        """
        Fetches Posts and Comments from Instagram and Analyzes their Sentiment.
        """
        try:
            self.username = username
            self.password = password
            
            if self.AuthCredential():
                profile = instaloader.Profile.from_username(self.instaloader.context, self.username)
                
                posts = []
                for post in profile.get_posts():
                    post_info = {
                        "Post_ID": post.shortcode,
                        "Post_Text": post.caption or "",
                        "Post_Date": post.date_utc,
                        "Likes_Count": post.likes,
                        "Comments_Count": post.comments,
                        "Comments": [comment.text for comment in post.get_comments()],
                        "Image_URL": post.url,
                        "Post_URL": f"https://www.instagram.com/p/{post.shortcode}/"
                    }
                    posts.append(post_info)                
                df = pd.DataFrame(posts)
                df = self.sentiment_analyzer.analyze(df)
                
                return df, True
            else:
                return pd.DataFrame(), False
        except Exception as e:
            logging.error("Error in Fetching Data: ", exc_info=e)
            return pd.DataFrame(), False