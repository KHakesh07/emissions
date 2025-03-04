import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Import modules
from modules.material import show_material_calculator
from modules.transport import show_transport_calculator
from modules.food import show_food_calculator

# Import visualizations
from visualizations.material_visualization import visual as material_visual
from visualizations.transportation_visualization import transport_visual
from visualizations.electricity_visualization import electricity_visual
from visualizations.food_visualization import food_visual

# Set page configuration
st.set_page_config(
    page_title="Emission Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


##############################################
# Database Initialization Function
##############################################
def create_database():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        conn = sqlite3.connect('data/emissions.db')
        cursor = conn.cursor()
        if os.path.exists('data/emissions.sql'):
            with open('data/emissions.sql', 'r') as file:
                sql_script = file.read()
            cursor.executescript(sql_script)
            conn.commit()
        else:
            st.warning("Database schema file not found. Database may not be properly initialized.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while creating the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Initialize the database
create_database()


##############################################
# Simple Login with Role Selection (in sidebar)
##############################################
def simple_login():
    # If already logged in, return the stored user
    if "logged_in_user" in st.session_state:
        return st.session_state.logged_in_user

    st.sidebar.header("Login")
    
    # Role selection from a drop-down
    role = st.sidebar.selectbox(
        "Select Your Role:",
        options=["Operations Manager", "Event Coordinator", "Sustainability Consultant"]
    )
    # Mapping: selected role -> expected username
    role_mapping = {
        "Operations Manager": "ops_manager",
        "Event Coordinator": "event_coordinator",
        "Sustainability Consultant": "sustain_consultant"
    }

    # Get username and password input
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")
    login_button = st.sidebar.button("Login", key="login_button")
    
    if login_button:
        # Validate: username (case-insensitive match) and password
        if username.strip().lower() == role_mapping[role] and password == "admin123":
            st.sidebar.success(f"Logged in as {role}")
            st.session_state.logged_in_user = role_mapping[role]
            return st.session_state.logged_in_user
        else:
            st.sidebar.error("Invalid role, username, or password")
            return None
    else:
        return None


def call():
    # Call the simple login function
    logged_in_user = simple_login()
    if not logged_in_user:
        st.stop()
    
    ####################################################
    # Post-Login Sidebar UI: Welcome, Profile, Support, Logout
    ####################################################
    with st.sidebar:
        st.markdown("---")
        st.title(f"Welcome, {logged_in_user}")
        # Additional buttons (Profile, Contact Us) can be indexed here.
        st.button("Profile", key="profile_button")
        st.button("Contact Us", key="support_button")
        if st.button("Logout", key="logout_button"):
            # Remove logged_in_user from session state and refresh the page.
            if "logged_in_user" in st.session_state:
                del st.session_state.logged_in_user
            # Use HTML meta refresh to force a page reload.
            st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

def scope3():

    ##############################################
    # Main Dashboard Section (Accessible to All Logged-In Users)
    ##############################################
    st.title("Emission Calculator")

    # Calculations Section: Four tabs for each calculator
    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "Material Calculator", "Transport Calculator", "Food Calculator"
    ])
    with calc_tab1:
        show_material_calculator()
    with calc_tab2:
        show_transport_calculator()
    with calc_tab3:
        show_food_calculator()

    # Emission Analysis Section: Four tabs for visualizations
    st.header("Emission Analysis")
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
