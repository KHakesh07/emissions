import streamlit as st

##############################################
# Simple Login with Role Selection (in Sidebar)
##############################################
def simple_login():
    # If already logged in, immediately return the stored user
    if "logged_in_user" in st.session_state:
        return st.session_state.logged_in_user

    st.sidebar.header("Login")

    # Role selection from a drop-down
    role = st.sidebar.selectbox(
        "Select Your Role:",
        options=["Operations Manager", "Event Coordinator", "Sustainability Consultant"]
    )
    # Map role selection to the expected username
    role_mapping = {
        "Operations Manager": "ops_manager",
        "Event Coordinator": "event_coordinator",
        "Sustainability Consultant": "sustain_consultant"
    }

    # Username and password input fields
    username = st.sidebar.text_input("Username:")
    password = st.sidebar.text_input("Password:", type="password")
    login_button = st.sidebar.button("Login", key="login_button")

    if login_button:
        if username.strip().lower() == role_mapping[role] and password == "admin123":
            st.sidebar.success(f"Logged in as {role}")
            st.session_state.logged_in_user = role_mapping[role]
            return st.session_state.logged_in_user
        else:
            st.sidebar.error("Invalid role, username, or password")
            return None
    else:
        return None

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