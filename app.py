# Set page configuration as the very first Streamlit command.
import streamlit as st
st.set_page_config(
    page_title="Emission Calculator and Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


import time
from streamlit_option_menu import option_menu

from app_pages.scope3 import scope3_page
from app_pages.scope2 import scope2_page
from app_pages.scope1 import scope1_page
from app_pages.overview import overview_page
from app_pages.Login import simple_login
from visualizations.OverallAnalysis import vis


#----------------------#
# Data base initiation #
#----------------------#
from common import create_database
create_database()

# Main page title and description in the main area.
st.title("Emission Calculator and Analysis Dashboard")
st.write("This dashboard is designed to calculate and analyze emissions for Scope 1, Scope 2, and Scope 3.")


##############################################
# Call Function: Handles Login and sets up Sidebar UI after login
##############################################
def call():
    user = simple_login()
    if not user:
        # Instead of halting execution, return False so the caller knows login didn’t succeed.
        return False

    # Post-Login Sidebar UI: Replace login form with welcome message and additional options.
    with st.sidebar:
        st.markdown("---")
        st.title(f"Welcome, {user}")
        st.button("Profile", key="profile_button")
        st.button("Contact Us", key="support_button")
        if st.button("Logout", key="logout_button"):
            if "logged_in_user" in st.session_state:
                del st.session_state.logged_in_user
            # Force a reload using an HTML meta refresh.
            st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
    return True

# -------------------------------
# Sidebar: Show Login or Post-Login UI
# -------------------------------
call()

# -------------------------------
# Main Content: Option Menu Navigation
# -------------------------------
# Create an option menu for navigation.
selected = option_menu(
    menu_title="Emissions Calculators",
    menu_icon="cloud",
    options=["Overview", "Scope 1", "Scope 2", "Scope 3", "Analysis"],
    orientation="horizontal",
)


# Routing based on selection
if selected == "Overview":
    overview_page()
elif selected == "Scope 1":
    scope1_page()
elif selected == "Scope 2":
    scope2_page()
elif selected == "Scope 3":
    scope3_page()
elif selected == "Analysis":
    vis()