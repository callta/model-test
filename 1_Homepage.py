import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import cloudpickle

# Configure
st.set_page_config(
    page_title="UCL models",
    initial_sidebar_state="collapsed")

# Remove the Streamlit menu
# st.markdown(""" <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style> """, unsafe_allow_html=True)

if "shared" not in st.session_state:
   st.session_state["shared"] = True

# Title
st.title('Predicting lung cancer risk')

# st.markdown("""<h1 style='text-align: center; color: black;'>Predicting lung cancer risk</h1>""", unsafe_allow_html=True)

# Information
st.markdown("""
        This software can help determine who might be eligible for
        lung cancer screening based on a personalised estimate
        of their risk of lung cancer.
        
        It is intended for use by individuals who have smoked at least 100
        cigarettes in their lifetime and have not been diagnosed with lung cancer.

        To find out more, please see the About section or have a look
         at this [paper](http://dx.doi.org/10.1101/2023.01.27.23284974).
        """)

st.info("""        
        This software uses a risk prediction model to produce estimates.
        Note that no risk prediction model is 100% accurate. 
        Some individuals with a low predicted risk of a condition 
        will go on to develop this condition, and conversely, 
        some people with a high predicted risk of a condition 
        will never develop the condition.
        """)

st.warning("""**Disclaimer**: In accessing and/or using this software, 
            you expressly acknowledge and agree that 
            you have read and accepted
            the disclaimer. You can navigate to the disclaimer 
            using the sidebar of this webpage.""")

st.divider()

st.header("Run analysis")

st.session_state["model_name"] = st.selectbox(
    'Select a model to use for predictions (defaults to UCL-D):',
    ("UCL-D", "UCL-I")
)

next = st.button("Please click here to start the analysis.", use_container_width=True)
if next:
    switch_page("Age")
