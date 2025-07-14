import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import check_auth, login
from utils.helpers import load_data, calculate_metrics

# Enforce login
authenticated, role = check_auth()
if not authenticated:
    login()
    st.stop()

df = load_data("data/outreach_data.csv")
metrics = calculate_metrics(df)

st.title("📊 Daily/Weekly Outreach Metrics")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("Total Outreach", metrics["Total Outreach"])
col2.metric("Meetings Booked", metrics["Meetings Booked"])
col3.metric("Opportunity Rate (%)", metrics["Opportunity Rate (%)"])
col4.metric("Conversion Rate (%)", metrics["Conversion Rate (%)"])
col5.metric("Follow-Ups Made", metrics["Follow-Ups Made"])
col6.metric("New Leads Generated", metrics["New Leads Generated"])

# Trend Chart with Chart Type Toggle
st.markdown("### 📅 Outreach Trend")

chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Histogram", "Pie"])

if chart_type == "Line":
    fig = px.line(df, x="date", y="outreach_volume", title="Outreach Volume Over Time")
elif chart_type == "Bar":
    fig = px.bar(df, x="date", y="outreach_volume", title="Outreach Volume Over Time")
elif chart_type == "Histogram":
    fig = px.histogram(df, x="outreach_volume", nbins=20, title="Outreach Volume Distribution")
elif chart_type == "Pie":
    pie_df = df.groupby("date")["outreach_volume"].sum().reset_index()
    fig = px.pie(pie_df, names="date", values="outreach_volume", title="Outreach Volume by Date")

st.plotly_chart(fig, use_container_width=True)
