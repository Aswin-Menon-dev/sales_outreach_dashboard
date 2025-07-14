import streamlit as st
import pandas as pd
import os
import io
from datetime import date
from utils.auth import check_auth, login

# --- Enforce login ---
authenticated, role = check_auth()
if not authenticated:
    login()
    st.stop()

# --- Constants ---
REQUIRED_COLUMNS = [
    "date", "outreach_volume", "meetings_booked",
    "qualified_meetings", "closed_deals", "follow_ups", "new_leads"
]
DATA_PATH = "data/outreach_data.csv"

st.title("📤 Data Upload & Manual Entry")

# --- Admin Reset Button ---
if role == "admin":
    st.warning("⚠️ Admin Panel: Dangerous Operation")
    if st.button("🗑️ Clear All Data (Admin Only)"):
        if os.path.exists(DATA_PATH):
            os.remove(DATA_PATH)
            st.success("✅ Data file cleared successfully.")
            st.experimental_rerun()

# --- Download Excel Template ---
st.markdown("### 📄 Download Sample Template")
sample_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    sample_df.to_excel(writer, index=False, sheet_name="Template")
buffer.seek(0)

st.download_button(
    label="Download Excel Template",
    data=buffer,
    file_name="outreach_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- Upload Section ---
st.markdown("### 📥 Upload Excel or CSV")
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Ensure required columns are present
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            st.error(f"❌ Missing required columns: {REQUIRED_COLUMNS}")
        else:
            # Convert 'date' to date type
            df["date"] = pd.to_datetime(df["date"]).dt.date

            # Check for null dates
            if df["date"].isnull().any():
                st.error("❌ Some rows have empty 'date' fields.")
            else:
                st.success("✅ File validated. Preview below:")
                st.dataframe(df)

                # Remove duplicate dates
                if os.path.exists(DATA_PATH):
                    existing = pd.read_csv(DATA_PATH, parse_dates=["date"])
                    existing["date"] = pd.to_datetime(existing["date"]).dt.date
                    duplicates = df["date"].isin(existing["date"])
                    if duplicates.any():
                        st.warning("⚠️ Some dates already exist. They will be excluded.")
                        df = df[~duplicates]

                if df.empty:
                    st.info("ℹ️ No new data to append after removing duplicates.")
                elif st.button("Append Uploaded Data"):
                    if os.path.exists(DATA_PATH):
                        updated_df = pd.concat([existing, df], ignore_index=True)
                    else:
                        updated_df = df
                    updated_df.to_csv(DATA_PATH, index=False)
                    st.success(f"✅ Appended {len(df)} rows successfully!")
                    st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

# --- Manual Data Entry ---
st.markdown("### ✍️ Enter Data Manually")
with st.form("manual_data_entry"):
    manual_date = st.date_input("Date", value=date.today())
    outreach_volume = st.number_input("Outreach Volume", min_value=0)
    meetings_booked = st.number_input("Meetings Booked", min_value=0)
    qualified_meetings = st.number_input("Qualified Meetings", min_value=0)
    closed_deals = st.number_input("Closed Deals", min_value=0)
    follow_ups = st.number_input("Follow-Ups Made", min_value=0)
    new_leads = st.number_input("New Leads Generated", min_value=0)
    submit = st.form_submit_button("Submit Entry")

if submit:
    new_entry = pd.DataFrame([{
        "date": manual_date,
        "outreach_volume": outreach_volume,
        "meetings_booked": meetings_booked,
        "qualified_meetings": qualified_meetings,
        "closed_deals": closed_deals,
        "follow_ups": follow_ups,
        "new_leads": new_leads
    }])

    if os.path.exists(DATA_PATH):
        existing = pd.read_csv(DATA_PATH, parse_dates=["date"])
        existing["date"] = pd.to_datetime(existing["date"]).dt.date
        if manual_date in existing["date"].values:
            st.error("❌ An entry with this date already exists.")
        else:
            updated_df = pd.concat([existing, new_entry], ignore_index=True)
            updated_df.to_csv(DATA_PATH, index=False)
            st.success("✅ Manual entry added successfully.")
            st.experimental_rerun()
    else:
        new_entry.to_csv(DATA_PATH, index=False)
        st.success("✅ Manual entry added successfully.")
        st.experimental_rerun()
