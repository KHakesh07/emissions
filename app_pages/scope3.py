import streamlit as st
from modules.material import show_material_calculator
from modules.transport import show_transport_calculator
from modules.food import show_food_calculator
from visualizations.material_visualization import visualize
from visualizations.transportation_visualization import transport_visual
from visualizations.food_visualization import food_visual
import sqlite3
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from visualizations.logistics import logist_vis

def scope3_page():
    if "logged_in_user" not in st.session_state:
        st.error("Please login first!")
        return
    st.title("Scope 3 Emission")
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
    vis_tab1, vis_tab2, vis_tab3, vis_tab4 = st.tabs([
        "Transportation","logistics", "Materials", "Foods and Vegetables"
    ],)
    with vis_tab1:
        transport_visual("TransportEmissions")
    with vis_tab2:
        logist_vis()
    with vis_tab3:
        conn = sqlite3.connect("data/emissions.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Materials")
        data1 = cur.fetchall()
        conn.close()
        st.subheader("Data:")
        df = pd.DataFrame(data1, columns=["id","event", "Category", "Weight", "Quantity", "Emission","Timestamp"])
        dataframe = dataframe_explorer(df)
        st.dataframe(dataframe, use_container_width=True)
        fig = px.pie(df, names='event', values="Emission", color="Weight", title="Emissions Breakdown", hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

        category = st.selectbox("Select a category", ["Trophies", "Banners", "Momentoes", "Kit"], key="Hake")
        visualize(category)
    with vis_tab4:
        food_visual()
