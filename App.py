import os
import time
import logging
import requests
import streamlit as st
from dotenv import load_dotenv

from frontend.src.Input import Input
from frontend.src.Header import Header
from frontend.src.SubHeader import SubHeader
from frontend.src.LoginHeader import LoginHeader
from frontend.charts.BarChart import BarChart
from frontend.charts.GroupedBarChart import GroupedBarChart
from frontend.charts.PieChart import PieChart

# Loading Environment Variables
load_dotenv(".env")

class InstaMotionUI:
    def __init__(self) -> None:
        """
        Initializes the InstaMotionUI Class
        """
        self.Title = os.getenv("TITLE")
        self.SERVER_URL = os.getenv("SENTIMENT_ANAYSIS_API")
        self.Username = ""
        self.Password = ""
        self.AnalyzeButton = False

    def Custom_CSS(self) -> None:
        """Custom CSS Styles"""
        st.markdown("""
            <style>
                .stMarkdown, .stForm {
                    min-width: 300px;
                }
                .login-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    margin-top: -20%;
                    margin-bottom: 20%;
                }
                .login-form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 10px;
                    width: 100%;
                }
                .container-with-margin {
                    margin-bottom: 10%;
                }
                .alert {
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

    def LoginForm(self) -> None:
        """Creates the Login form for Instagram Credentials."""
        try:
            self.Custom_CSS()

            with st.container():
                st.markdown('<div class="login-container">', unsafe_allow_html=True)

                with st.form(key='login_form'):
                    LoginHeader()

                    self.Username = Input(label="Username", placeholder="Enter Instagram Username", input_type="default", key='username')
                    self.Password = Input(label="Password", placeholder="Enter Instagram Password", input_type="password", key='password')

                    self.AnalyzeButton = st.form_submit_button(label='Analyze')
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            logging.error("An Error Occurred in LoginForm", exc_info=e)
            raise e

    def AnalysisCharts(self, post: dict) -> None:
        """Displays Charts based on the Analysis of the Instagram Post."""
        try:
            with st.container():
                st.markdown(f"""<h4>Post Link: <a href="{post["Post_URL"]}">{post["Post_URL"]}</a></h4>""", unsafe_allow_html=True)

            with st.container():
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Likes & Comment Count")
                    with st.spinner("Rendering Bar Chart..."):
                        BarChart([post["Likes_Count"], post["Comments_Count"]])

                with col2:
                    st.write("Caption Analysis")
                    with st.spinner("Rendering Pie Chart..."):
                        PieChart(post["Post_Text_Label"])

            with st.container():
                st.write("Comments Analysis")
                with st.spinner("Rendering Grouped Bar Chart..."):
                    GroupedBarChart(post["Comments_Label"])

                st.markdown('<div class="container-with-margin"></div>', unsafe_allow_html=True)
        except Exception as e:
            logging.error("An Error Occurred in AnalysisCharts", exc_info=e)
            raise e

    def InstaMotionUI(self) -> None:
        """Main function to run the Instagram sentiment analysis UI."""
        try:
            Header(self.Title)
            SubHeader()
            self.LoginForm()

            if self.AnalyzeButton:
                if self.Username and self.Password:
                    with st.spinner("Processing..."):
                        response = requests.post(self.SERVER_URL, json={"username": self.Username, "password": self.Password}).json()
                        posts, bool = response["response"][0], response["response"][1]
                        
                        if bool: 
                           posts_info = posts
                           Header(f"Hey {self.Username}")
   
                           for post in posts_info:
                               self.AnalysisCharts(post)
   
                           success = st.success("Sentiment Analysis Completed Successfully.")
                           time.sleep(2); success.empty();
                        else:
                           error = st.error("Invalid Credentials Request Blocked by Instagram")
                           time.sleep(2); error.empty();
                else:
                    error = st.error("Please Enter both Username and Password.")
                    time.sleep(2); error.empty();

            st.markdown('<div class="alert">Remember to keep your Instagram Credentials Safe and use this Tool Responsibly.</div>', unsafe_allow_html=True)
        except Exception as e:
            logging.error("An Error Occurred in InstaMotionUI", exc_info=e)
            raise e

if __name__ == "__main__":
    
    App = InstaMotionUI()
    App.InstaMotionUI()