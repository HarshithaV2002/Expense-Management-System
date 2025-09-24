import streamlit as st
from datetime import datetime
import requests



API_URL = "http://127.0.0.1:8000"


def add_tab():
    choose_date = st.date_input(
        "Enter date", datetime(2024, 8, 1),
        label_visibility="collapsed",
        key="add_date"
    )

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="add_expense_form"):
        st.write("Enter new expenses for the date")

        expenses = []
        for i in range(5):  # allow up to 5 new expenses
            amount, category, notes = 0.0, "Shopping", ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    "Amount", min_value=0.0, step=1.0, value=amount,
                    key=f"amount_{i}", label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    "Category", options=categories,
                    index=categories.index(category),
                    key=f"category_{i}", label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    "Notes", value=notes,
                    key=f"notes_{i}", label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Add Expenses")
        if submit_button:
            new_expenses = [expense for expense in expenses if expense['amount'] > 0]
            if new_expenses:
                response = requests.post(f"{API_URL}/expense/{choose_date}", json=new_expenses)
                if response.status_code in (200, 201):
                    st.success("New expenses added successfully!")
                else:
                    st.error("Failed to add expenses.")
            else:
                st.warning("No expenses entered.")
