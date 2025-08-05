import streamlit as st
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Panel")

password = st.text_input("Enter admin password", type="password")
if password != "admin123":
    st.warning("Access denied")
    st.stop()

uploaded_file = st.file_uploader("Upload Camper Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    required_cols = {"Name", "Camp", "Status", "Check-in Time"}

    if not required_cols.issubset(df.columns):
        st.error("Excel must include: Name, Camp, Status, Check-in Time")
    else:
        selected_camp = st.selectbox("View campers by camp", sorted(df["Camp"].unique()))
        st.write(f"### Campers in {selected_camp}")
        st.dataframe(df[df["Camp"] == selected_camp])

        st.download_button(
            label="⬇️ Download Updated Sheet",
            data=df.to_excel(index=False),
            file_name="updated_checkins.xlsx"
        )
