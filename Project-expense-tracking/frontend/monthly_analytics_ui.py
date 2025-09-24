# import requests
# import streamlit as st
# import pandas as pd
#
#
# API_URL = "http://127.0.0.1:8000"
#
# def monthly_analytics_tab():
#     st.title("Expense Breakdown By Category")
#
#     response = requests.get(f"{API_URL}/analytics/")
#     monthly_expenses = response.json().get("Summary", [])
#     df = pd.DataFrame(monthly_expenses)
#     df.index = df.index + 1
#     df.rename(columns={
#         "Month":"Month",
#         "Total":"Total"
#     })
#
#     # df.index.name = "S.No"
#     df_sorted = df.sort_values(by="Month", ascending=True)
#     df_sorted.set_index("Month",inplace=True)
#     st.bar_chart(data=df_sorted.set_index("Month")['Total'], width=0, height=0, use_container_width=True)
#
#     df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
#
#     st.table(df_sorted.sort_index())
#
#
#
#
#
#     # st.bar_chart(data=df.set_index("Month")['Total'], width=0, height=0, use_container_width=True)
#     # st.dataframe(df, use_container_width=True)
#
#
#
#
#









import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def monthly_analytics_tab():
    # Fetch data from API
    response = requests.get(f"{API_URL}/analytics/")
    if response.status_code != 200:
        st.error("Failed to retrieve monthly summary")
        return

    monthly_summary = response.json()  # expecting list of dicts like [{"month_name": "January", "total": 1200}, ...]

    if not monthly_summary:
        st.warning("No monthly expenses found")
        return

    # Create DataFrame
    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "month_name": "Month",
        "total": "Total"
    }, inplace=True)

    # Ensure calendar order
    df["Month"] = pd.Categorical(
        df["Month"],
        categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        ordered=True
    )
    df.sort_values("Month", inplace=True)

    # Add serial number
    df.index = df.index + 1
    df.index.name = "S.No"

    # Bar chart
    st.title("Expense Breakdown By Months")
    st.bar_chart(data=df.set_index("Month")["Total"], use_container_width=True)

    # Format Total column
    df["Total"] = df["Total"].map("{:.2f}".format)

    # Display table
    st.table(df)
