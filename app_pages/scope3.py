import streamlit as st
from modules.material import show_material_calculator
from modules.transport import show_transport_calculator
from modules.food import show_food_calculator
from visualizations.material_visualization import visual as material_visual
from visualizations.transportation_visualization import transport_visual
from visualizations.food_visualization import food_visual

def scope3_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please login first!")
        return
    st.subheader("Scope 3 Emission Calculator")
    # Calculations Section: Tabs for each calculator
    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "Material Calculator", "Transport Calculator", "Food Calculator"
    ])
    with calc_tab1:
        show_material_calculator()
    with calc_tab2:
        show_transport_calculator()
    with calc_tab3:
        show_food_calculator()

    st.header("Emission Analysis")
    # Emission Analysis Section: Tabs for visualizations
    vis_tab1, vis_tab2, vis_tab3 = st.tabs([
        "Transportation", "Materials", "Foods and Vegetables"
    ])
    with vis_tab1:
        transport_visual("TransportEmissions")
    with vis_tab2:
        table = st.selectbox("Select a Category:", 
                             ["Trophies", "Banners", "Momentoes", "PetWaterBottle", "Kit", "Kitems"])
        material_visual(table)
    with vis_tab3:
        food_visual()