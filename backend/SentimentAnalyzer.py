import re
import torch
import logging
import requests
import instaloader
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from PIL import Image
from io import BytesIO
from torchvision import transforms
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

torch.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

class ModifiedResNet(nn.Module):
    def __init__(self, num_classes):
        super(ModifiedResNet, self).__init__()
        self.resnet = models.resnet50(pretrained=True)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)

    def forward(self, x):
        try:
            return self.resnet(x)
        except Exception as e:
            logging.error("An Error Occurred in ModifiedResNet: ", exc_info=e)
            raise e

class SentimentAnalyzer:
    def __init__(self) -> None:
        self.Text_Model_Name = 'bert-base-uncased'
        self.Text_Model = BertForSequenceClassification.from_pretrained(self.Text_Model_Name, num_labels=2)
        self.Text_Tokenizer = BertTokenizer.from_pretrained(self.Text_Model_Name)
        self.Text_Classifier = pipeline('sentiment-analysis', model=self.Text_Model, tokenizer=self.Text_Tokenizer)
        
        self.Image_Model = ModifiedResNet(num_classes=2)
        self.Image_Model.eval()
        
        self.Image_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        self.Sentiment_Labels = [
            'Negative', 'Positive'
        ]
        
    def MentionRemover(self, text):
        try:
            text = re.sub(r"[@()]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            return text
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def HashtagRemover(self, text):
        try:
            return re.sub(r"#\w+", "", text).strip()
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def RefineText(self, text):
        try:
            text = self.MentionRemover(text)
            text = self.HashtagRemover(text)
            return text
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def Analyze_Text_Sentiment(self, text):
        try:
            result = self.Text_Classifier(text)
            sentiment = result[0]['label']
            return 'Positive' if sentiment == 'LABEL_0' else 'Negative'
        except Exception as e:
            logging.error("An Error Occurred in Analyze Text Sentiment: ", exc_info=e)
            raise e
    
    def Analyze_Image_Sentiment(self, image_url):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content)).convert('RGB')
            image = self.Image_transform(image).unsqueeze(0)
            
            with torch.no_grad():
                features = self.Image_Model(image)
                probabilities = F.softmax(features, dim=1)
                sentiment_idx = torch.argmax(probabilities, dim=1).item()
                sentiment = self.Sentiment_Labels[sentiment_idx]
            return sentiment
        except Exception as e:
            logging.error("An Error Occurred in Analyze Image Sentiment: ", exc_info=e)
            raise e
        
    def Analyze(self, df):
        try:
            results = []
            for index, row in df.iterrows():
                row['Post_Text'] = self.RefineText(row['Post_Text'])
                row['Comments'] = [self.RefineText(comment) for comment in row['Comments']]
                
                Text_Sentiment = self.Analyze_Text_Sentiment(row['Post_Text'])
                Image_Sentiment = self.Analyze_Image_Sentiment(row['Image_URL'])
                
                # For Test
                print(Text_Sentiment, Image_Sentiment)
                
                results.append({
                    'Post_ID': row['Post_ID'],
                    'Post_Text': row['Post_Text'],
                    'Post_Date': row['Post_Date'],
                    'Likes_Count': row['Likes_Count'],
                    'Comments_Count': row['Comments_Count'],
                    'Comments': row['Comments'],
                    'Image_URL': row['Image_URL'],
                    'Text_Sentiment': Text_Sentiment,
                    'Image_Sentiment': Image_Sentiment
                })
                
            return pd.DataFrame(results)
        except Exception as e:
            logging.error("An Error Occurred in Analyze: ", exc_info=e)
            raise e
        
class FetchData:
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()
        self.Username = None
        self.Password = None
        
    def AuthCredential(self):
        try:
            try:
                self.L.login(self.Username, self.Password)
                return True
            except Exception:
                return False
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
    def run(self, username, password):
        try:
            self.Username = username
            self.Password = password
            
            if self.AuthCredential():
                profile = instaloader.Profile.from_username(self.L.context, self.Username)
                
                posts = []
                for post in profile.get_posts():
                    post_info = {
                        "Post_ID": post.shortcode,
                        "Post_Text": post.caption,
                        "Post_Date": post.date_utc,
                        "Likes_Count": post.likes,
                        "Comments_Count": post.comments,
                        "Comments": [comment.text for comment in post.get_comments()],
                        "Image_URL": post.url
                    }
                    posts.append(post_info)                
                df = pd.DataFrame(posts)
                
                sentiment = SentimentAnalyzer()
                sentiment_df = sentiment.Analyze(df)
                return sentiment_df, True
            else:
                return pd.DataFrame(), False
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
if __name__=="__main__":
    
    username = 'aniketsahu_02'
    password = 'Ani02@'
    
    Obj = FetchData()
    df, bool = Obj.run(username, password)
    
    # print(df)