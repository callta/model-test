import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Configure
st.set_page_config(
    page_title="UCL models - About",
    initial_sidebar_state="collapsed")

# Remove the Streamlit menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# Title
st.title('About')

st.header("Who is this software for?")

st.markdown("""
        This software is designed to be used 
        to predict the risk of dlung cancer in 
        an individual who has smoked at least 100 
        cigarettes in their lifetime and are
        aged at least 40 years old.         
        """)

st.header("How does this software work?")

st.markdown("""
        This software uses a risk prediction model
        to predict the risk of developing lung cancer (UCL-I)
        or dying from lung cancer (UCL-D)
        within the next 5 years.

        The model uses information about your age, the
        number of years you have smoked, and the number of 
        pack-years you have smoked to make predictions. A pack-year is defined
        as smoking one packet of 20 cigarettes per day for
        one year. 

        The software automatically calculates pack-years
        from the number of years you have smoked and the
        average number of cigarettes you smoke(d) per day.

        For more details, please read the 
        following [paper](http://dx.doi.org/10.1101/2023.01.27.23284974).
        """)

st.header("Who developed the risk prediction model?")

st.markdown("""
        This model was developed by researchers in the
        Department of Respiratory Medicine at UCL and
        the Cambridge Centre for AI in Medicine (CCAIM)
        at the University of Cambridge.
        """)