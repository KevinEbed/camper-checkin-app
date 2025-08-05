import pandas as pd
from datetime import datetime

EXCEL_PATH = "uploaded_files/latest_camper_data.xlsx"

def load_camper_data():
    try:
        df = pd.read_excel(EXCEL_PATH)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Camp", "Check-in Status", "Check-in Time"])

def save_camper_data(df):
    df.to_excel(EXCEL_PATH, index=False)

def check_in_camper(name, camp):
    df = load_camper_data()
    df.loc[(df["Name"] == name) & (df["Camp"] == camp), "Check-in Status"] = "Checked-in"
    df.loc[(df["Name"] == name) & (df["Camp"] == camp), "Check-in Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_camper_data(df)
