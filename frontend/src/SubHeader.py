import logging
import streamlit as st

def SubHeader() -> None:
    """
    Renders a Sub-Header with an Informational Message in Streamlit App.
    """
    try:
        # Sub-Title with Informational Message
        st.write("Enter Instagram Username and Password to see the Sentiment Analysis of Posts and Comments.")
    except Exception as e:
        logging.error("An error occurred while rendering the Sub-Header component: ", exc_info=e)
        raise e