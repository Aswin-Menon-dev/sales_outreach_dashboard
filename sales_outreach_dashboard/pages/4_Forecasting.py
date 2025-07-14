import streamlit as st
import pandas as pd
from prophet import Prophet
from utils.auth import check_auth, login
from utils.helpers import load_data
import plotly.graph_objects as go

# Enforce login
authenticated, role = check_auth()
if not authenticated:
    login()
    st.stop()

st.title("📈 Forecasting Outreach Volume")

df = load_data("data/outreach_data.csv")
df_prophet = df.rename(columns={"date": "ds", "outreach_volume": "y"})

m = Prophet()
m.fit(df_prophet)
future = m.make_future_dataframe(periods=7)
forecast = m.predict(future)

chart_type = st.selectbox("Select Forecast Chart Type", ["Line", "Bar"], key="forecast_chart_type")

fig = go.Figure()
if chart_type == "Line":
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['outreach_volume'], name='Actual'))
else:
    fig.add_trace(go.Bar(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
    fig.add_trace(go.Bar(x=df['date'], y=df['outreach_volume'], name='Actual'))

st.plotly_chart(fig, use_container_width=True)
