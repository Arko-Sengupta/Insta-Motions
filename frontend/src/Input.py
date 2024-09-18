import logging
import streamlit as st

def Input(label: str, placeholder: str, key: str, input_type: str = "default") -> str:
    """
    Renders Input Field with a Label and Placeholder in a Streamlit App.
    """
    try:
        # Custom CSS for Input Field and Label
        st.markdown("""
        <style>
        .input-field {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 5px;
            padding: 0.5rem;
        }
        .required {
            color: red;
            font-size: 1.2rem;
            margin-left: 5px;
        }
        .input-label {
            display: flex;
            align-items: center;
            margin-bottom: -50px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render the Label with a Required Asterisk
        st.markdown(f'''<div class="input-label">{label} <span class="required">*</span></div>''', unsafe_allow_html=True)
        
        # Render the Input Field
        if input_type == "password":
            field = st.text_input("", placeholder=placeholder, type="password", key=key)
        else:
            field = st.text_input("", placeholder=placeholder, key=key)
        
        return field
    except Exception as e:
        logging.error("An Error Occurred while rendering the Input Component: ", exc_info=e)
        raise e
