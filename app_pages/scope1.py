import streamlit as st
from modules.sc1_emissions import display_scope1
from visualizations.scope_1Visual import display

def scope1_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please login to access the dashboard.")
        return
    display_scope1()
    display()