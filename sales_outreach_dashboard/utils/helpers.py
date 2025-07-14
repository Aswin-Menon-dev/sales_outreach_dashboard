import os
import pandas as pd

def load_data(file_path):
    # Get the absolute path to the CSV relative to the repo root
    root_path = os.path.dirname(os.path.dirname(__file__))  # One level up from utils/
    full_path = os.path.join(root_path, file_path)

    # Create the file if it doesn't exist (optional fallback)
    if not os.path.exists(full_path):
        cols = [
            "date", "outreach_volume", "meetings_booked",
            "qualified_meetings", "closed_deals", "follow_ups", "new_leads"
        ]
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        pd.DataFrame(columns=cols).to_csv(full_path, index=False)

    return pd.read_csv(full_path, parse_dates=["date"])


def calculate_metrics(df):
    total_outreach = df["outreach_volume"].sum()
    total_meetings = df["meetings_booked"].sum()
    total_qualified = df["qualified_meetings"].sum()
    total_closed = df["closed_deals"].sum()
    total_followups = df["follow_ups"].sum()
    total_leads = df["new_leads"].sum()

    opportunity_rate = (total_qualified / total_meetings) * 100 if total_meetings else 0
    conversion_rate = (total_closed / total_qualified) * 100 if total_qualified else 0

    return {
        "outreach_volume": total_outreach,
        "meetings_booked": total_meetings,
        "qualified_meetings": total_qualified,
        "closed_deals": total_closed,
        "follow_ups": total_followups,
        "new_leads": total_leads,
        "opportunity_rate": round(opportunity_rate, 2),
        "conversion_rate": round(conversion_rate, 2),
    }
