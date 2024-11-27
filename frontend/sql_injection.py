import streamlit as st
import requests

base_url = "http://127.0.0.1:8000/"

def search_user(name):
    response = requests.get(f"{base_url}sql_injection/{name}")
    if response.status_code == 200:
        return response.json().get("users", None)
    else:
        return {"error": "Failed to fetch data"}

st.title("Let's inject some sql;")
user_name = st.text_input("Enter the name to search", value="natalka'; SELECT * FROM FriendGroup WHERE '1'='1")

if st.button("submit"):
    result = search_user(user_name)
    st.write(result)