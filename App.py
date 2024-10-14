import json
import os
import time
import logging
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from frontend.src.Header import Header
from frontend.src.SubHeader import SubHeader
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
        self.AnalyzeButton = False
        self.df = None

    def Custom_CSS(self) -> None:
        """Custom CSS Styles"""
        st.markdown("""
            <style>
                .stMarkdown, .stForm {
                    min-width: 300px;
                }
                .upload-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    margin-top: -20%;
                    margin-bottom: 20%;
                }
                .container-with-margin {
                    margin-bottom: 10%;
                }
                .alert {
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

    def Upload_XLSX_File(self) -> None:
        """Component to Upload Excel File and Send its Content in a POST Request."""
        try:
            self.Custom_CSS()
            st.markdown('<div class="upload-container">', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Choose an Excel File", type="xlsx")
            
            if uploaded_file is not None:
                try:
                    self.df = pd.read_excel(uploaded_file, engine='openpyxl')
                    
                    success = st.success("File Successfully Uploaded!")
                    time.sleep(2)
                    success.empty()
                    
                    st.dataframe(self.df)
                    self.AnalyzeButton = st.button("Analyze Data")
                except Exception as e:
                    st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            logging.error("An Error Occurred in Upload_XLSX_File", exc_info=e)
            raise e

    def AnalysisCharts(self, post: dict) -> None:
        """Displays Charts based on the Analysis of the Instagram Post."""
        try:
            with st.container():
                st.markdown(f"""<h4>Post Link: <a href="{post["Post_URL"]}">{"Click Here"}</a></h4>""", unsafe_allow_html=True)

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
        """Main Function to Run the Instagram Sentiment Analysis UI."""
        try:
            Header(self.Title)
            SubHeader()
            self.Upload_XLSX_File()

            if self.AnalyzeButton and self.df is not None:
                with st.spinner("Processing..."):
                    try:
                        self.df['Post_ID'] = self.df['Post_ID'].astype(str)
                        self.df['Post_Text'] = self.df['Post_Text'].astype(str)
                        self.df['Post_Date'] = self.df['Post_Date'].astype(str)
                        self.df['Likes_Count'] = self.df['Likes_Count'].astype(int)
                        self.df['Comments_Count'] = self.df['Comments_Count'].astype(int)
                        
                        
                        data = self.df.to_dict(orient='records')
                        response = requests.post(self.SERVER_URL, json={"data": data})
                        
                        if response.status_code == 200:
                            response = response.json()
                            posts_info = json.loads(response["response"])
                            
                            Header("Data Analysis")

                            for post in posts_info:
                                self.AnalysisCharts(post)

                            success = st.success("Sentiment Analysis Completed Successfully.")
                            time.sleep(2)
                            success.empty()
                        else:
                            error = st.error("Error in Data Analysis.")
                            time.sleep(2)
                            error.empty()

                    except Exception as e:
                        error = st.error("Failed to Send Data to the Server.")
                        time.sleep(2)
                        error.empty()
                        
                        logging.error("Error Sending Data to Server", exc_info=e)

            st.markdown('<div class="alert">Upload Data for Analysis and View the Results Here.</div>', unsafe_allow_html=True)
        except Exception as e:
            logging.error("An Error Occurred in InstaMotionUI", exc_info=e)
            raise e

if __name__ == "__main__":
    
    App = InstaMotionUI()
    App.InstaMotionUI()