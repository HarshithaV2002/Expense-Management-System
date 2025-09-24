import streamlit as st
from datetime import datetime
import requests


API_URL = "http://127.0.0.1:8000"


def delete_tab():

    delete_date = st.date_input(
        "Choose date to delete expenses", datetime(2024, 8, 1),
        key="delete_date_tab4" , label_visibility="collapsed"
    )

    container = st.container()

    with container:
        response = requests.get(f"{API_URL}/expense/{delete_date}")
        if response.status_code == 200:
            expenses = response.json()
        else:
            st.error("Failed to retrieve expenses")
            expenses = []

        if expenses:
            col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
            with col1:
                st.markdown("**Amount**")
            with col2:
                st.markdown("**Category**")
            with col3:
                st.markdown("**Notes**")
            with col4:
                st.markdown("**Delete**")

            for i, exp in enumerate(expenses):
                exp_id = exp.get("id", i)
                amount = exp["amount"]
                category = exp["category"]
                notes = exp["notes"]

                col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
                with col1:
                    st.text(amount)
                with col2:
                    st.text(category)
                with col3:
                    st.text(notes)
                with col4:
                    delete_btn = st.button("Delete", key=f"delete_btn_{i}_{exp_id}")

                if delete_btn:
                    res = requests.delete(f"{API_URL}/expense/{delete_date}/{exp_id}")
                    if res.status_code == 200:
                        st.success("Expense deleted successfully!")

                        st.session_state['refresh_delete_tab'] = not st.session_state.get('refresh_delete_tab', False)
                    else:
                        st.error(f"Failed to delete expense: {res.text}")


            col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
            with col1:
                st.text("")
            with col2:
                st.text("")
            with col3:
                st.text("")
            with col4:
                delete_all_btn = st.button("DELETE ALL", key="delete")

            if delete_all_btn:
                res = requests.delete(f"{API_URL}/expense/{delete_date}")
                if res.status_code == 200:
                    st.success("All expenses for this date deleted successfully!")
                    st.session_state['refresh_delete_tab'] = not st.session_state.get('refresh_delete_tab', False)
                else:
                    st.error(f"Failed to delete expenses: {res.text}")

        else:
            st.info("No expenses found for this date.")
