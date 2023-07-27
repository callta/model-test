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

st.header("How many cigarettes do you / did you smoke per day, on average?")

if "cigarettes_per_day" not in st.session_state:
    st.session_state._cigarettes_per_day = 0

def on_change_store():
    st.session_state._cigarettes_per_day = st.session_state.cigarettes_per_day

# smoking_intensity = st.text_input(
#     label="How many cigarettes do you / did you smoke per day, on average?", 
#     key="cigarettes_per_day",
#     label_visibility="hidden", 
#     placeholder="Please enter how many cigarettes do you / did you smoke per day (on average) here",
#     on_change=on_change_store)

smoking_intensity = st.number_input(
    label="Please enter the number of cigarettes you do or did smoke (if you no longer smoke) on average each day:", 
    key="cigarettes_per_day",
    # label_visibility="hidden", 
    value = 0,
    on_change=on_change_store,
    help="""
        For information, a packet of cigarettes typically contains 20 cigarettes.

        If you smoke(d) only occasionally, consider how many cigarettes
        you have in the average month and divide this by 30 to produce an 
        estimated daily average.
    """
    )
    
col1, col2, col3, col4, col5 = st.columns(5)

if smoking_intensity:
    if st.session_state._cigarettes_per_day >= 70:

        with col1: 
            st.write(f"""Please verify you smoke {st.session_state._cigarettes_per_day} cigarettes per day and then press next.""")

        with col2:
            next = st.button("Next", use_container_width=True)
            if next:
                switch_page("Results")

    elif st.session_state._cigarettes_per_day < 0:
        st.write(f"""
        
        You have entered that you have smoke no cigarettes
        on average per day. 
        
        If you smoke(d) only occasionally, consider how many cigarettes
        you have in the average month and divide this by 30.
        """)
    else:
        switch_page("Results")


with col1:
    back = st.button("Back", use_container_width=True)
    if back:
        switch_page("Smoking duration")

# with col5:
#     next = st.button("Next", use_container_width=True)
#     if next:
#         switch_page("Results")





