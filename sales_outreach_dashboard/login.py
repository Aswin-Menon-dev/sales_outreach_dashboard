import streamlit as st
from utils.auth import login, check_auth

# --- Set page config ---
st.set_page_config(
    page_title="Login",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Show login form in sidebar ---
login()

# --- Check login status ---
authenticated, role = check_auth()

# --- Display appropriate message ---
if authenticated:
    st.success(f"✅ Welcome {role.capitalize()}!")
else:
    st.title("🔐 Login Required")
    st.markdown("""
    👉 Please click the **arrow at the top right** to open the **sidebar** and log in.  
    Once logged in, you'll be able to access all sections of the dashboard from the sidebar.
    """)
