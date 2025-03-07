import streamlit as st
from modules.electricity import show_electricity_hvac_calculator
from visualizations.electricity_visualization import electricity_visual


def scope2_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please Login before access")
        return 
    st.subheader("Scope 2 Calculator")
    show_electricity_hvac_calculator()
    st.header("Emission Analysis")
    electricity_visual()