import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import check_auth, login
from utils.helpers import load_data

# Enforce login
authenticated, role = check_auth()
if not authenticated:
    login()
    st.stop()

df = load_data("data/outreach_data.csv")

st.title("📂 Reports & Export")

# Filters
st.sidebar.header("Filter")
date_range = st.sidebar.date_input("Date Range", [df['date'].min(), df['date'].max()])
filtered_df = df[(df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]

st.markdown("### 📥 Download Data")
st.download_button("Download CSV", filtered_df.to_csv(index=False), file_name="outreach_report_filtered.csv")

st.markdown("### 📊 Filtered Table")
st.dataframe(filtered_df)

# Chart Toggle
st.markdown("### 📈 Visualize Filtered Outreach Volume")

chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Histogram", "Pie"], key="report_chart_type")

if chart_type == "Line":
    fig = px.line(filtered_df, x="date", y="outreach_volume", title="Outreach Volume Over Time")
elif chart_type == "Bar":
    fig = px.bar(filtered_df, x="date", y="outreach_volume", title="Outreach Volume Over Time")
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x="outreach_volume", nbins=20, title="Outreach Volume Distribution")
elif chart_type == "Pie":
    pie_df = filtered_df.groupby("date")["outreach_volume"].sum().reset_index()
    fig = px.pie(pie_df, names="date", values="outreach_volume", title="Outreach Volume by Date")

st.plotly_chart(fig, use_container_width=True)
