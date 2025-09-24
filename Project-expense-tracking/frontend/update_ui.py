import streamlit as st
from datetime import datetime
import requests


API_URL = "http://127.0.0.1:8000"


def update_tab():
    update_date = st.date_input(
        "Choose date", datetime(2024, 8, 1),
        key="update_date_tab3" , label_visibility="collapsed"
    )
    response = requests.get(f"{API_URL}/expense/{update_date}")
    if response.status_code == 200:
        expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    if expenses:
        col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
        with col1:
            st.markdown("**Amount**")
        with col2:
            st.markdown("**Category**")
        with col3:
            st.markdown("**Notes**")
        with col4:
            st.markdown("**Update**")


        for i in range(5):
            if i < len(expenses):
                exp = expenses[i]
                exp_id = exp.get("id", i)
                amount = exp["amount"]
                category = exp["category"]
                notes = exp["notes"]
            else:

                exp_id = None
                amount, category, notes = 0.0, "Shopping", ""


            col1, col2, col3, col4 = st.columns([2, 2, 3, 2])

            with col1:
                new_amount = st.number_input(
                    "", min_value=0.0, step=1.0,
                    value=amount, key=f"amount_{i}_{exp_id}"
                )
            with col2:
                index = categories.index(category) if category in categories else 0
                new_category = st.selectbox(
                    "", options=categories, index=index, key=f"category_{i}_{exp_id}"
                )
            with col3:
                new_notes = st.text_input("", value=notes, key=f"notes_{i}_{exp_id}")
            with col4:
                submit_update = st.button("Update", key=f"update_btn_{i}_{exp_id}")

            if submit_update:
                if exp_id is not None:
                    payload = {
                        "id": exp_id,
                        "amount": new_amount,
                        "category": new_category,
                        "notes": new_notes,
                        "expense_date": str(update_date)
                    }
                    res = requests.post(f"{API_URL}/expense/{update_date}/{exp_id}", json=payload)
                    if res.status_code == 200:
                        st.success(f"Expense updated successfully!")
                    else:
                        st.error(f"Failed to update expense! Status code: {res.status_code} - {res.text}")
                else:
                    st.warning("This row is empty and cannot be updated.")
    else:
        st.info("No expenses found for this date.")

