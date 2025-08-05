import streamlit as st
import pandas as pd
from utils import load_camper_data, check_in_camper

st.set_page_config(page_title="Camper Check-in", page_icon="🎒")

st.title("🎒 Camper Check-in")

df = load_camper_data()

if df.empty:
    st.error("No camper data uploaded yet. Please contact the admin.")
else:
    camp_list = df["Camp"].unique()
    selected_camp = st.selectbox("🏕 Select your camp", sorted(camp_list))

    filtered_df = df[df["Camp"] == selected_camp]
    camper_names = filtered_df["Name"].sort_values().tolist()
    selected_name = st.selectbox("🔍 Search for your name", camper_names)

    if st.button("✅ Check In"):
        check_in_camper(selected_name, selected_camp)
        st.success(f"{selected_name} checked in successfully!")
