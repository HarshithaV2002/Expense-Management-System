import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"


def read_tab():
    select_date = st.date_input("Enter date", datetime(2024, 8, 1), label_visibility="collapsed", key="read_date")
    response = requests.get(f"{API_URL}/expense/{select_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        df = pd.DataFrame(existing_expenses)
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        df = df.rename(columns={
            "amount": "Amount",
            "category": "Category",
            "notes": "Notes",
        })
        df.index = df.index + 1
        df.index.name = "S.No"
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []



