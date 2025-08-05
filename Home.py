import streamlit as st
import pandas as pd
from datetime import datetime
import os


st.write("📂 Current Working Directory:", os.getcwd())

excel_file = os.path.join("uploaded_files", "latest_camper_data.xlsx")
st.write("🔍 Looking for file at:", excel_file)

if not os.path.exists(excel_file):
    st.error("❌ Camper data file not found. Please contact the admin.")
    st.stop()
else:
    st.success("✅ Camper file found!")

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="Camper Check-in", page_icon="🎒", layout="centered")
st.title("🎒 Camper Check-in")

# ------------------ Load Camper Data ------------------ #
excel_file = os.path.join("uploaded_files", "latest_camper_data.xlsx")

if not os.path.exists(excel_file):
    st.error("❌ Camper data file not found. Please contact the admin.")
    st.stop()

try:
    df = pd.read_excel(excel_file)
except Exception as e:
    st.error(f"❌ Error reading camper data file: {e}")
    st.stop()

# ------------------ Validate Required Columns ------------------ #
required_columns = ["Name", "Camp", "Status", "Check-in Time"]
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"❌ Missing columns in data file: {', '.join(missing_cols)}")
    st.stop()

# ------------------ Camper Check-in Form ------------------ #
camper_name = st.selectbox("Select Your Name", sorted(df["Name"].dropna().unique()))

if st.button("Check In"):
    idx = df[df["Name"] == camper_name].index

    if not idx.empty:
        row = idx[0]
        if str(df.at[row, "Status"]).lower() == "checked-in":
            st.warning("⚠️ You are already checked in.")
        else:
            df.at[row, "Status"] = "Checked-in"
            df.at[row, "Check-in Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                df.to_excel(excel_file, index=False)
                st.success("✅ You have been successfully checked in!")
            except Exception as e:
                st.error(f"❌ Error saving check-in: {e}")
    else:
        st.error("❌ Name not found in the camper list.")
