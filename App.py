import time
import logging
import streamlit as st
import matplotlib.pyplot as plt

from frontend.src.Input import Input
from frontend.src.Header import Header
from frontend.src.SubHeader import SubHeader
from frontend.src.LoginHeader import LoginHeader

class InstaMotionUI:
    def __init__(self) -> None:
        pass
    
    def LoginForm(self):
        try:
            # Custom CSS for Form
            st.markdown("""
                <style>
                .login-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                .login-form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 10px;
                    width: 100%;
                }
                </style>
                """, unsafe_allow_html=True)
            
            # Wrap Login Form into a Responsive Flexbox
            with st.container():
                st.markdown('<div class="login-container">', unsafe_allow_html=True)
                
                with st.form(key='login_form'):
                    LoginHeader()
                    
                    self.Username = Input(label="Username", placeholder="Enter Instagram Username", input_type="default", key='username')
                    self.Password = Input(label="Password", placeholder="Enter Instagram Password", input_type="password", key='password')
                    
                    self.AnalyzeButton = st.form_submit_button(label='Analyze')
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            logging.error("An Error Occurred", exc_info=e)
            raise e

        
    def Dummy(self):
            Header("Instagram Sentiment Analysis")
            SubHeader()
            self.LoginForm()
            
            if self.AnalyzeButton:
               if self.Username and self.Password:
                   with st.spinner("Processing..."):
                       posts_info = [
                           {
                               "Post_ID": "kkjbjlcvev",
                               "Post_Text": "Had a great day at the beach!",
                               "Post_Date": "02-09-2024",
                               "Likes_Count": 120,
                               "Comments_Count": 15,
                               "Comments": ["Awesome", "Horrible weather"],
                               "Image_URL": "https://example.com/image1",
                               "Post_URL": f"https://www.instagram.com/p/kkjbjlcvev/",
                               "Post_Text_Label":[0.8, 0.1, 0.1],
                               "Comments_Label": {"Awesome": [0.8, 0.1, 0.1], "Horrible weather": [0.1, 0.1, 0.8]}
                           }
                       ]
                       
                       for i, post in enumerate(posts_info):
                           # Unpacking data
                           post_text = post["Post_Text"]
                           likes_count = post["Likes_Count"]
                           comments_count = post["Comments_Count"]
                           post_sentiment = post["Post_Text_Label"]
                           comments_sentiment = post["Comments_Label"]
                           
                           # 1. Bar chart for Likes and Comments Count
                           fig, ax = plt.subplots(figsize=(6, 4))
                           ax.bar(["Likes", "Comments"], [likes_count, comments_count], color=['blue', 'green'])
                           ax.set_title(f"Likes and Comments Count for Post: {post['Post_ID']}")
                           ax.set_ylabel("Count")
                           st.pyplot(fig)
                           
                           # 2. Pie chart for Post Text Sentiment Analysis
                           labels = ["Positive", "Neutral", "Negative"]
                           fig, ax = plt.subplots(figsize=(6, 6))
                           ax.pie(post_sentiment, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'gray', 'red'])
                           ax.set_title(f"Post Sentiment Analysis: {post_text}")
                           st.pyplot(fig)
                           
                           # 3. Grouped Bar Chart for Comments Sentiment Analysis
                           comments = list(comments_sentiment.keys())
                           positive_sentiments = [comments_sentiment[comment][0] for comment in comments]
                           neutral_sentiments = [comments_sentiment[comment][1] for comment in comments]
                           negative_sentiments = [comments_sentiment[comment][2] for comment in comments]
                           
                           fig, ax = plt.subplots(figsize=(8, 6))
                           bar_width = 0.25
                           index = range(len(comments))
                           
                           bar1 = ax.bar(index, positive_sentiments, bar_width, label="Positive", color='green')
                           bar2 = ax.bar([i + bar_width for i in index], neutral_sentiments, bar_width, label="Neutral", color='gray')
                           bar3 = ax.bar([i + 2 * bar_width for i in index], negative_sentiments, bar_width, label="Negative", color='red')
                           
                           ax.set_xlabel('Comments')
                           ax.set_title('Sentiment Analysis for Comments')
                           ax.set_xticks([i + bar_width for i in index])
                           ax.set_xticklabels(comments)
                           ax.legend()
                           
                           st.pyplot(fig)
                           
                       success = st.success("Sentiment analysis completed successfully.")
                       time.sleep(5)
                       success.empty()
               else:
                   st.error("Please enter both username and password.")
            # Dismissible Alert (Using Streamlit's markdown for basic customization)
            st.markdown('<div class="alert">Remember to keep your Instagram credentials safe and use this tool responsibly.</div>', unsafe_allow_html=True)
            
if __name__=="__main__":
    
    App = InstaMotionUI()
    App.Dummy()
