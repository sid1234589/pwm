import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from pathlib import Path

# File to store client data
data_file = Path("clients.csv")

# Load data or initialize
if data_file.exists():
    df = pd.read_csv(data_file, parse_dates=["Request Date", "Processed Date"])
else:
    df = pd.DataFrame(columns=[
        "Client ID", "Client Name", "Country", "Account Type",
        "KYC", "ID Proof", "FATCA", "Risk Level", "Request Date",
        "Processed Date", "TAT", "Maintenance", "Closure Status",
        "Closure Date", "Approver"
    ])

# Set page config
st.set_page_config(page_title="PWM Lifecycle Tracker", layout="wide")

# Title
st.title("🔐 PWM Client Lifecycle Tracker")

# ✅ One clean form
with st.expander("➕ Add New Client"):
    with st.form("new_client_form"):
        st.subheader("Client Onboarding")
        cols = st.columns(2)
        client_id = cols[0].text_input("Client ID")
        name = cols[1].text_input("Client Name")
        country = cols[0].selectbox("Country", ["India", "USA", "UAE", "China", "UK", "Singapore", "Pakistan"])
        acc_type = cols[1].selectbox("Account Type", ["Individual", "Joint", "Trust"])
        kyc = cols[0].selectbox("KYC", ["✅", "❌"])
        id_proof = cols[1].selectbox("ID Proof", ["✅", "❌"])
        fatca = cols[0].selectbox("FATCA", ["✅", "❌"])
        request_date = cols[1].date_input("Request Date", datetime.date.today())
        processed_date = cols[0].date_input("Processed Date", datetime.date.today())

        submitted = st.form_submit_button("Add Client")
        if submitted:
            tat = (processed_date - request_date).days
            risk = "High" if kyc == "❌" or id_proof == "❌" else ("Medium" if fatca == "❌" else "Low")
            new_client = pd.DataFrame([{
                "Client ID": client_id,
                "Client Name": name,
                "Country": country,
                "Account Type": acc_type,
                "KYC": kyc,
                "ID Proof": id_proof,
                "FATCA": fatca,
                "Risk Level": risk,
                "Request Date": request_date,
                "Processed Date": processed_date,
                "TAT": tat,
                "Maintenance": "-",
                "Closure Status": "-",
                "Closure Date": "",
                "Approver": ""
            }])
            df = pd.concat([df, new_client], ignore_index=True)
            df.to_csv(data_file, index=False)
            st.success("✅ Client added successfully")

# KPI Summary
st.header("📊 Summary Dashboard")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Clients", len(df))
kpi2.metric("Accounts Opened", len(df[df["Client ID"].notna()]))
kpi3.metric("Avg TAT", round(df["TAT"].mean(), 2) if not df.empty else 0)
kpi4.metric("Maintenance Reqs", len(df[df["Maintenance"] != "-"]))
kpi5.metric("High Risk", len(df[df["Risk Level"] == "High"]))

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 TAT per Client")
    if not df.empty:
        fig_tat = px.line(df, x="Client Name", y="TAT", markers=True, title="Turnaround Time by Client")
        st.plotly_chart(fig_tat, use_container_width=True)

with chart_col2:
    st.subheader("🧯 Risk Level Distribution")
    if not df.empty:
        fig_risk = px.pie(df, names="Risk Level", title="Risk Breakdown")
        st.plotly_chart(fig_risk, use_container_width=True)

# Client Table (fix for Streamlit Cloud)
st.subheader("📁 Client Data")
if not df.empty:
    safe_df = df.copy()
    safe_df["Request Date"] = safe_df["Request Date"].astype(str)
    safe_df["Processed Date"] = safe_df["Processed Date"].astype(str)
    st.dataframe(safe_df)
else:
    st.info("No client data found yet.")
