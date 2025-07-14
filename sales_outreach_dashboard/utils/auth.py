import streamlit as st

def login():
    # If already logged in, show logout only
    if st.session_state.get("logged_in"):
        username = st.session_state.get("username", "User")
        st.sidebar.success(f"Logged in as {username} ({st.session_state.get('role')})")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()
        return

    # Show login form
    st.sidebar.title("🔐 Login")

    with st.sidebar.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")  # Submit on Enter too ✅

    if submit:
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"
            st.session_state["username"] = username
            st.success("✅ Login successful as Admin")
            st.rerun()
        else:
            st.session_state["logged_in"] = False
            st.error("❌ Invalid credentials")

def check_auth():
    return st.session_state.get("logged_in", False), st.session_state.get("role", None)
