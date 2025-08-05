import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Panel")

# Password protection
password = st.text_input("Enter admin password", type="password")
if password != "admin123":
    st.warning("Access denied")
    st.stop()

# File uploader
uploaded_file = st.file_uploader("Upload Camper Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        required_cols = {"Name", "Camp", "Status", "Check-in Time"}
        actual_cols = set(df.columns.str.strip())  # Strip whitespace

        # Check for missing columns (case-insensitive, strip whitespace)
        normalized_df_cols = {col.strip().lower() for col in df.columns}
        normalized_required_cols = {col.lower() for col in required_cols}

        if not normalized_required_cols.issubset(normalized_df_cols):
            st.error("❌ Excel must include: Name, Camp, Status, Check-in Time")
        else:
            selected_camp = st.selectbox("View campers by camp", sorted(df["Camp"].unique()))
            filtered_df = df[df["Camp"] == selected_camp]

            st.write(f"### Campers in {selected_camp}")
            st.dataframe(filtered_df)

            # Prepare Excel file for download
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            st.download_button(
                label="⬇️ Download Updated Sheet",
                data=buffer,
                file_name="updated_checkins.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
