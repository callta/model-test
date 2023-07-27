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

st.header("Age")

if "age" not in st.session_state:
    st.session_state._age = 0

def on_change_store():
    st.session_state._age = st.session_state.age

# age = st.text_input(
#     label="Age", key="age", label_visibility="hidden", 
#     placeholder="Please enter your age here", 
#     on_change=on_change_store)

# age_float = np.fromstring(st.session_state._age)

age = st.number_input(
    label="Please enter your age in years here:", 
    key="age", 
    # label_visibility="hidden", 
    value = 0,
    on_change=on_change_store
    )

col1, col2, col3, col4, col5 = st.columns(5)

if age:
    if age < 40 or age > 75:
        st.write("This model is only valid for people aged between 40 and 75 years old. Please enter a valid age.")
        pass
    else:
        if age:
            switch_page("Smoking duration")

with col1:
    back = st.button("Back", use_container_width=True)
    if back:
        switch_page("Homepage")

# with col5:
#     next = st.button("Next", use_container_width=True)
#     if next:
#         switch_page("Smoking duration")
