import logging
import streamlit as st

def Header(title: str) -> None:
    """
    Renders Header with an Instagram Icon and the provided Title in a Streamlit App.
    """
    try:
        # Title with Font Awesome Instagram Icon
        st.markdown(f"""
        <style>
            /* Font Awesome import */
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

            /* Instagram Icon Styling */
            .instagram-icon {{
                font-size: 2rem;
                background: linear-gradient(135deg, #f58529, #dd2a7b, #8134af, #515bd4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-fill-color: transparent;
                margin-right: 10px;
            }}
            
            /* Heading Styling */
            h1 {{
                display: flex;
                align-items: center;
                font-size: 2rem;
                margin: 0;
            }}
            @media (max-width: 420px) {{
                h1 {{
                   font-size: 1rem;
                }}
            }}
        </style>
        <h1>
            <i class="fab fa-instagram instagram-icon"></i>
            {title}
        </h1>
        """, unsafe_allow_html=True)
    except Exception as e:
        logging.error("An Error Occurred while rendering the Header Component: ", exc_info=True)
        raise e