import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Camper Check-in", layout="centered")

# Title & Instructions
st.title("🎒 Camper Check-in System")
st.markdown("Upload the Excel sheet with camper data and allow campers to check in.")

# Upload Excel File
uploaded_file = st.file_uploader("📂 Upload the Camper Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Read Excel File
    df = pd.read_excel(uploaded_file)
    
    # Ensure required columns exist
    required_columns = {"Name", "Camp", "Status", "Check-in Time"}
    if not required_columns.issubset(df.columns):
        st.error(f"Excel sheet must contain columns: {', '.join(required_columns)}")
    else:
        # Sidebar Admin View
        with st.sidebar:
            st.header("🛠️ Admin Panel")
            selected_camp_admin = st.selectbox("Select Camp to View", sorted(df["Camp"].unique()))
            filtered_admin = df[df["Camp"] == selected_camp_admin]
            st.write("### Campers in this camp:")
            st.dataframe(filtered_admin.reset_index(drop=True), use_container_width=True)
            st.download_button("⬇️ Download Updated Sheet", data=df.to_excel(index=False), file_name="Updated_Checkin_List.xlsx")

        # Camper Check-in Section
        st.subheader("👋 Camper Check-in")
        selected_camp = st.selectbox("Select Your Camp", sorted(df["Camp"].unique()))
        campers_in_camp = df[df["Camp"] == selected_camp]["Name"].tolist()
        selected_name = st.selectbox("Select Your Name", campers_in_camp)

        if st.button("✅ Check In"):
            idx = df[(df["Camp"] == selected_camp) & (df["Name"] == selected_name)].index
            if len(idx) > 0:
                if df.loc[idx[0], "Status"] == "Checked-in ✅":
                    st.warning("You already checked in.")
                else:
                    df.at[idx[0], "Status"] = "Checked-in ✅"
                    df.at[idx[0], "Check-in Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"{selected_name}, you are now checked in!")
            else:
                st.error("Camper not found.")
