import streamlit as st
import requests

base_url = "http://localhost:8000/"

if "user_groups" not in st.session_state:
    st.session_state.user_groups = []

st.title("Group Management")
st.header("Hi, Add your group!")

with st.form(key="create_group_form"):
    group_name = st.text_input("Group name:")

    if st.form_submit_button("Create!"):
        if group_name:
            try:
                response = requests.post(f"{base_url}create_group/", json = {"group_name": group_name, "username": st.session_state.user.username})
                if response.status_code == 200:
                    st.success("Group created!")
                else:
                    st.error(f"Group creation failed: {response.json().get('message', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please fill all fields!")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Add friends!")
    with st.form(key="group_form"):
        selected_group = st.selectbox("Choose a group", st.session_state.user.friendgroups.keys())
        username = st.text_input("Friend's username:", placeholder="Enter a username")
        submit_button = st.form_submit_button("Add member!")

    if submit_button:
        if username:
            response = requests.post(f"{base_url}add_user_to_group/", json = {"fg_id": st.session_state.user.friendgroups[selected_group], "username": username})
            message = response.json().get("message", "")
            st.info(message)
        else:
            st.error("Please enter a username!")


with col2:
    st.subheader("Other Actions")
    if st.button("Refresh your groups"):
        try:
            response = requests.get(f"{base_url}user_friendgroups/{st.session_state.user.username}")
            if response.status_code == 200:
                print(response.json())
                st.session_state.user.friendgroups = response.json().get("friend_groups", {})
                st.success("Groups Refreshed!")
                st.rerun()
            else:
                st.error(f"Refresh failed: {response.json().get('message', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

st.markdown("---")