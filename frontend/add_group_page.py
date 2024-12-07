import streamlit as st

potential_members = ()

st.header("Hi, Add your group!")

group_name = st.text_input("Group name:")
st.button("Create!")

st.selectbox("Choose member", potential_members)
st.button("Add member!")