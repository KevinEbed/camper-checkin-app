import streamlit as st
import pandas as pd
from utils import load_camper_data, save_camper_data
from io import BytesIO

st.set_page_config(page_title="Admin Dashboard", page_icon="🔐")

st.title("🔐 Admin Dashboard")

uploaded_file = st.file_uploader("📤 Upload Camper Excel List", type=["xlsx"])

if uploaded_file:
    df_uploaded = pd.read_excel(uploaded_file)
    save_camper_data(df_uploaded)
    st.success("Camper list uploaded and saved!")

st.markdown("---")
st.header("📊 Camper Check-in Status")

df = load_camper_data()

if df.empty:
    st.warning("No camper data available.")
else:
    st.dataframe(df, use_container_width=True)

    # Download updated sheet
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("📥 Download Updated List", buffer.getvalue(), file_name="updated_checkin_list.xlsx", mime="application/vnd.ms-excel")
