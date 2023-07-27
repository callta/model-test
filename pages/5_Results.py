import pandas as pd
import numpy as np
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import cloudpickle

# Configure
st.set_page_config(
    page_title="Results",
    initial_sidebar_state="collapsed")

# Remove the Streamlit menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


if st.session_state["_age"] == 0 or st.session_state["_smoking_duration"] == 0 or st.session_state["_cigarettes_per_day"] == 0:
    st.write("Please return to the homepage and enter your information.")
    pass

else:
    # Load model and cache
    def load_model_from_file(path):
        with open(path, "rb") as f:
            return cloudpickle.load(f)
        
    # with st.spinner("Running analyses..."):
    @st.cache_resource(show_spinner="Loading...")
    def predict(model):

        if model == "UCL-D":
            return load_model_from_file(f"models/ucld/fittedmodel.p")
        elif model == "UCL-I":
            return load_model_from_file(f"models/ucli/fittedmodel.p")

    model = predict(model=st.session_state["model_name"])
    st.session_state["model"] = model

    # Calculate pack-years from smoking duration and smoking intensity
    packyears = np.float64(st.session_state["_smoking_duration"]) * np.float64(st.session_state["_cigarettes_per_day"]) / 20

    # Put this into a dataframe and feed into model
    X = pd.DataFrame({
        "age": [st.session_state["_age"]],
        "smoking_duration": [st.session_state["_smoking_duration"]],
        "pack_years": [packyears]
    })

    pred = st.session_state["model"].predict_proba(X)[1]

    # Display results
    if st.session_state["model_name"] == "UCL-D":
        st.subheader("Predicted risk of death from lung cancer within five years:")
    else:
        st.subheader("Predicted risk of developing lung cancer within five years:")
    st.metric("", f"{np.round(pred[0] * 100, 2)}%")

    st.divider()

    st.markdown(f"""
        These results are based on the following information you provided: 

    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Age", st.session_state["_age"])
    with col2:
        st.metric("Years smoked", st.session_state["_smoking_duration"])
    with col3:
        st.metric("Cigarettes/day", st.session_state["_cigarettes_per_day"])

    st.markdown(f"""
        If any of these are incorrect, please return to the homepage and re-enter your information.

    """)

    st.divider()


# Return to homepage button
col1, col2, col3, col4 = st.columns((1,1,1,1))
with col4:
    return_home = st.button("Return to homepage")
    if return_home:
        switch_page("Homepage")