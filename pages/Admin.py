import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Panel")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_file = st.file_uploader("📤 Upload Camper Excel File", type=["xlsx"])
if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(UPLOAD_DIR, f"campers_list_{timestamp}.xlsx")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.session_state["latest_uploaded_file"] = file_path
    st.success(f"✅ File uploaded: {file_path}")

latest_file = st.session_state.get("latest_uploaded_file", None)

if latest_file and os.path.exists(latest_file):
    df = pd.read_excel(latest_file)

    # Camp filter dropdown
    camps = df["Camp"].dropna().unique()
    selected_camp = st.selectbox("🏕️ Filter by Camp", ["All"] + list(camps))

    if selected_camp != "All":
        df = df[df["Camp"] == selected_camp]

    st.dataframe(df, use_container_width=True)

    # Download updated file
    st.download_button(
        label="📥 Download Updated Check-in Sheet",
        data=df.to_excel(index=False),
        file_name="updated_checkin_list.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("⬆️ Please upload a camper Excel file to begin.")
