import streamlit as st
from modules.electricity import show_electricity_hvac_calculator
from visualizations.electricity_visualization import electricity_visual


def scope2_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please Login before access")
        return 
    st.title("Scope 1 Emission")
    st.write("Scope 2 emissions refer to indirect greenhouse gas (GHG) emissions resulting from purchased electricity, steam, heating, and cooling used by an organization. These emissions occur at the source of energy production but are accounted for by the company consuming the energy. Since organizations rely heavily on electricity for operations, reducing Scope 2 emissions often involves transitioning to renewable energy sources, improving energy efficiency, and purchasing carbon offsets or renewable energy certificates (RECs). Scope 2 emissions are critical to track because they often make up a significant portion of an organization's carbon footprint and are essential for sustainability reporting and compliance with global climate regulations.")
    st.subheader("Scope 2 Calculator")
    show_electricity_hvac_calculator()
    st.header("Emission Analysis")
    electricity_visual()
