import streamlit as st
from utils.auth import login, check_auth
from utils.helpers import load_data, calculate_metrics

# --- Authentication ---
login()
authenticated, role = check_auth()
if not authenticated:
    st.warning("🔒 Please log in to view this page.")
    st.stop()

# --- Load data ---
df = load_data("data/outreach_data.csv")
metrics = calculate_metrics(df)

# --- Title ---
st.title("📊 Daily/Weekly Outreach Metrics")

# --- Display metrics ---
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8 = st.columns(2)

col1.metric("Total Outreach", metrics["outreach_volume"])
col2.metric("Meetings Booked", metrics["meetings_booked"])
col3.metric("Qualified Meetings", metrics["qualified_meetings"])
col4.metric("Closed Deals", metrics["closed_deals"])
col5.metric("Follow-Ups Made", metrics["follow_ups"])
col6.metric("New Leads", metrics["new_leads"])
col7.metric("Opportunity Rate", f"{metrics['opportunity_rate']}%")
col8.metric("Conversion Rate", f"{metrics['conversion_rate']}%")
