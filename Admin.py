import streamlit as st
import pandas as pd
from io import BytesIO
import os

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

        # Normalize column names
        df.columns = df.columns.str.strip()
        normalized_df_cols = {col.strip().lower() for col in df.columns}
        normalized_required_cols = {col.lower() for col in required_cols}

        if not normalized_required_cols.issubset(normalized_df_cols):
            st.error("❌ Excel must include: Name, Camp, Status, Check-in Time")
        else:
            # Save uploaded file using its original name
            filename = uploaded_file.name
            save_path = os.path.join("uploaded_files", filename)
            os.makedirs("uploaded_files", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Store the path in session_state for camper.py to access
            st.session_state["uploaded_file_path"] = save_path

            st.success("✅ File uploaded and saved successfully.")

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
