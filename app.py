import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Camper Check-in", layout="centered")
st.title("🎒 Camper Check-in")

uploaded_file = st.file_uploader("Upload the Camper Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_cols = {"Name", "Camp", "Status", "Check-in Time"}
    if not required_cols.issubset(df.columns):
        st.error("Excel must include: Name, Camp, Status, Check-in Time")
    else:
        selected_camp = st.selectbox("Select your camp", sorted(df["Camp"].unique()))
        camper_names = df[df["Camp"] == selected_camp]["Name"].tolist()
        selected_name = st.selectbox("Select your name", camper_names)

        if st.button("✅ Check-in"):
            idx = df[(df["Name"] == selected_name) & (df["Camp"] == selected_camp)].index[0]
            if df.at[idx, "Status"] == "Checked-in ✅":
                st.warning("You have already checked in.")
            else:
                df.at[idx, "Status"] = "Checked-in ✅"
                df.at[idx, "Check-in Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success(f"{selected_name}, you're checked in!")
