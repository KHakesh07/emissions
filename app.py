import streamlit as st
from main import scope3, call
from streamlit_option_menu import option_menu
from modules.EmissionsOverview import Overview
from modules.electricity import show_electricity_hvac_calculator
from visualizations.electricity_visualization import electricity_visual

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
    call()
elif selected == "Scope 1":
    call()
    st.subheader("Scope 1")
    st.write("To be implemented")
    st.balloons()
elif selected == "Scope 2":
    call()
    st.subheader("Scope 2")
    show_electricity_hvac_calculator()
    st.header("Emission Analysis")
    electricity_visual()

elif selected == "Scope 3":
    call()
    scope3()

