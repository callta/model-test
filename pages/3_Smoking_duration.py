import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import numpy as np

st.set_page_config(
    page_title=st.session_state["model_name"],
    initial_sidebar_state="collapsed")

# Remove the Streamlit menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.header("How many years have you smoked for?")

if "smoking_duration" not in st.session_state:
    st.session_state._smoking_duration = 0

def on_change_store():
    st.session_state._smoking_duration = st.session_state.smoking_duration

# smoking_duration = st.text_input(
#     label="How many years have you smoked for?", 
#     key="smoking_duration",
#     label_visibility="hidden", 
#     placeholder="Please enter how many years you have smoked for here",
#     on_change=on_change_store)

smoking_duration = st.number_input(
    label="Please enter the total number of years you have smoked for here:", 
    key="smoking_duration",
    # label_visibility="hidden", 
    value = 0,
    on_change=on_change_store
    )

smoking_duration_more_than_age = st.session_state._smoking_duration > st.session_state._age
age_start = st.session_state._age - st.session_state._smoking_duration
started_smoking_less_than_10 = age_start < 10

if smoking_duration:
    if smoking_duration_more_than_age:
        st.write(f"""
        
        You have entered that you have smoked for
        {st.session_state._smoking_duration-st.session_state._age} 
        more years than you have been alive.

        Please enter a valid smoking duration or press 
        the back button to return to the previous page
        and re-enter your age.
        """)
    elif st.session_state._smoking_duration < 0:
        st.write(f"""
        
        You have entered that you have smoked for zero years.
        
        This prediction model is only valid for those who 
        have ever smoked.
        """)
    elif started_smoking_less_than_10:

        col1, col2, col3, col4, col5 = st.columns((4,1,1,1,1))

        with col1: 
            st.write(f"""
            
            You have entered that you started smoking at the age of
            {st.session_state._smoking_duration-st.session_state._age}. 
                    
            Please confirm that this is correct by pressing next.
            """)

        with col5:
            next = st.button("Next", use_container_width=False)
            if next:
                switch_page("Smoking intensity")

    else:
        switch_page("Smoking intensity")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    back = st.button("Back", use_container_width=True)
    if back:
        switch_page("Age")
