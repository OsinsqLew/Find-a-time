#streamlit run front_page.py

import streamlit as st
from datetime import date, timedelta

st.header("Hi, Add spare time: ")
date = st.date_input(
    "Date",
    min_value=date.today(),
    max_value=date.today() + timedelta(days=14),
    )
st_time = st.time_input("Start time")
end_time = st.time_input("End time")
color = st.color_picker("Choose your favourite color")
st.button("Save")
