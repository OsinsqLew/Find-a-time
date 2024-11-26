import streamlit as st

st.header("Hi, log in!")

login = st.text_input("Login:")
password = st.text_input("Password")

st.button("Log in!")
