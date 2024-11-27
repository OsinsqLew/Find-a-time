import streamlit as st
from datetime import date, timedelta
import requests

base_url = "http://localhost:8000/"

st.header("Hi, Add spare time: ")
with st.form(key="create_event_form"):
    date_input = st.date_input(
        "Date",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=14),
        )
    st_time = st.time_input("Start time")
    end_time = st.time_input("End time")
    color = st.color_picker("Choose your favourite color")
    if st.form_submit_button("Save"):

        date_str = date_input.strftime('%Y-%m-%d')
        st_time_str = st_time.strftime('%H:%M:%S')
        end_time_str = end_time.strftime('%H:%M:%S')

        response = requests.post(f"{base_url}add_freespot/", json = {"username": st.session_state.user.username, "day": date_str, "start": st_time_str, "end": end_time_str})

        if response.status_code == 200:
            st.success("Spare time added successfully!")
        else:
            st.error(f"Adding spare time failed: {response.json().get('message', 'Unknown error')}")

