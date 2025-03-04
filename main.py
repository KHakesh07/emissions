import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from material import show_material_calculator
from transport import show_transport_calculator
from electricity import show_electricity_hvac_calculator
from food import show_food_calculator
from material_visualization import visual
from Transportation_visualization import transport_visual
from Electricity_visualization import electricity_visual
from food_visualization import food_visual

# Function to create the database if not exists
def create_database():
    try:
        conn = sqlite3.connect("emissions.db")
        cursor = conn.cursor()
        with open("emissions.sql", 'r') as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred while creating the database: {e}")
    finally:
        conn.close()

def scope3():
    # Initialize Database
    create_database()

# Streamlit App Title
    st.title("Emission Calculator")

# Tabs for navigation
    tab1, tab2 = st.tabs(["Calculations", "Admin"])

# Calculation Section
    with tab1:
        if "page" not in st.session_state:
            st.session_state.page = "main"

        if st.session_state.page == "main":
            if st.button("Material Emission Calculator"):
                st.session_state.page = "material"
            elif st.button("Transport Emission Calculator"):
                st.session_state.page = "transport"
            elif st.button("Food Emission Calculator"):
                st.session_state.page = "food"
            elif st.button("Electricity Emission Calculator"):
                st.session_state.page = "electricity"

        if st.session_state.page == "material":
            show_material_calculator()
        elif st.session_state.page == "transport":
            show_transport_calculator()
        elif st.session_state.page == "electricity":
            show_electricity_hvac_calculator()
        elif st.session_state.page == "food":
            show_food_calculator()

    # Admin Section
    with tab2:
        st.header("📊 Emission Analysis")
        admin_access = st.text_input("Enter Admin Password:", type="password")

        if admin_access == "admin123":
            st.success("Access Granted!")

            tab1, tab2, tab3, tab4 = st.tabs(["Transportation", "Materials", "Foods and Vegetables", "Electricity"])

            with tab1:
                st.header("Transportation Emissions Analysis")
                transport_visual("TransportEmissions")
            with tab2:
                st.header("Materials Emission Analysis")
                table = st.selectbox("Select a Category:", ["Trophies", "Banners", "Momentoes", "PetWaterBottle", "Kit", "Kitems"])
                visual(table)
            with tab3:
                st.header("Foods and Vegetables Emission Analysis")
                food_visual()
            with tab4:
                st.header("Electricity Emission Analysis")
                table = st.selectbox("Select a Category:", ["Electricity Emissions", "HVAC Emissions"])
                electricity_visual(table)

        else:
            st.warning("Admin access required.")
    
