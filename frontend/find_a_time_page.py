import streamlit as st
import requests
from datetime import date

def get_free_spot(availabilities, min_length, min_users):
    result_str = ""
    user_count = 1
    for day, user_availabilities in availabilities.items():
        day_av = [0]*24*60
        for user, day_availabilities in user_availabilities.items():
            user_count += 1
            for spot in day_availabilities:
                start, end = spot
                start = start.split(":")
                start = int(start[0])*60 + int(start[1])
                end = end.split(":")
                end = int(end[0])*60 + int(end[1])
                for i in range(start, end):
                    day_av[i] = (day_av[i] + 1)%user_count
        i = 0
        while i < len(day_av):
            if day_av[i] >= min_users:
                start = i
                while i < len(day_av) and day_av[i] >= min_users:
                    i += 1
                if i - start >= min_length:
                    result_str += f"{day} {start//60:02}:{start%60:02} - {i//60:02}:{i%60:02}\n"
            i+=1
    if result_str == "":
        return "No available time found."
    return result_str

def show_availabilities(availabilities):
    result_str = ""
    for day, user_availabilities in availabilities.items():
        result_str += f"{day}:\n"
        for user, day_availabilities in user_availabilities.items():
            result_str += f"\t\t{user}:\n"
            for spot in day_availabilities:
                start, end = spot
                result_str += f"\t\t\t{start} - {end}\n"
    if result_str == "":
        return "No available time found."
    return result_str.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;").replace("\n", "<br>")

base_url = "http://localhost:8000/"

st.title("Find a time!")
st.header("Find a time for a meeting with your friends!")
with st.form("time_finder"):
    selected_group = st.selectbox("Select a group", st.session_state.user.friendgroups.keys())
    min_length = st.number_input("Minimum meeting length (in minutes):", min_value=1, value=30)
    min_users = st.number_input("Minimum number of users:", min_value=1, value=2)
    if st.form_submit_button("Find a time"):
        response = requests.post(f"{base_url}find_time/", json = {"fg_id": st.session_state.user.friendgroups[selected_group], "start_day": date.today().strftime('%Y-%m-%d')})
        if response.status_code == 200:
            aviability = response.json().get("freespots", [])
            st.text(get_free_spot(aviability, min_length, min_users))
        else:
            st.error(f"Finding time failed: {response.json().get('message', 'Unknown error')}")

st.header("... or check aviability for a specific day:")
with st.form("day-time"):
    selected_group = st.selectbox("Select a group", st.session_state.user.friendgroups)
    date = st.date_input("Show aviability for:")
    date_str = date.strftime('%Y-%m-%d')
    if st.form_submit_button("Show"):
        response = requests.post(f"{base_url}find_time/", json = {"fg_id": st.session_state.user.friendgroups[selected_group], "start_day": date_str, "end_day": date_str})
        if response.status_code == 200:
            st.markdown(show_availabilities(response.json().get("freespots", {})), unsafe_allow_html=True)