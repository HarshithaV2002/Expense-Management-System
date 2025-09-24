import streamlit as st
from read_ui import read_tab
from add_ui import add_tab
from update_ui import update_tab
from delete_ui import delete_tab
from analytics_ui import analytic_tab
from monthly_analytics_ui import monthly_analytics_tab
import base64

with open("bg_pic1.jpg", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()

# Apply as background with dark overlay
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



st.title("Expense Tracking System")


tab1, tab2, tab3, tab4, tab5 , tab6 = st.tabs(["View", "Add", "Update", "Delete", "Analytics By Category","Analytics By Month"])

with tab1:
    read_tab()

with tab2:
    add_tab()

with tab3:
    update_tab()

with tab4:
    delete_tab()

with tab5:
    analytic_tab()

with tab6:
    monthly_analytics_tab()