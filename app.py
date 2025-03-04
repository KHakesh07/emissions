import streamlit as st
from main import scope3
from streamlit_option_menu import option_menu
from EmissionsOverview import Overview

st.title("Emission Calculator and analysis Dashbaord")
st.write("This dashboard is designed to calculate and analyze the emissions of a scope1, scop2 and scope3")

selected = option_menu(
    menu_title="Emissions Calculators",
    menu_icon="emissions",
    options=["Overview", "Scope 1", "Scope 2", "Scope 3"],
    orientation="horizontal",
)

if selected == "Overview":
    Overview()
elif selected == "Scope 1":
    st.subheader("Scope 1")
    st.write("To be implemented")
    st.balloons()
elif selected == "Scope 2":
    st.subheader("Scope 2")
    st.write("To be implemented")
    st.balloons()
elif selected == "Scope 3":
    scope3()

