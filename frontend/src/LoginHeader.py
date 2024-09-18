import logging
import streamlit as st

def LoginHeader() -> None:
    """
    Renders Login Header in a Streamlit App.
    """
    try:
        # Custom Styles for Login Header
        st.markdown(f"""
        <style>
            /* Login Header Styling */
            .header {{
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                text-align: center;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Render the login Header
        st.markdown('<div class="header">Login</div>', unsafe_allow_html=True)
    
    except Exception as e:
        logging.error("An Error Occurred while rendering the Login Header Component: ", exc_info=True)
        raise e