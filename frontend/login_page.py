import streamlit as st
import requests
from Backend.User import User

base_url = "http://localhost:8000/"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.logged_in:
    st.header("Hi, log in!")
    st.write("If you do not have account now, please register.")

    login = st.text_input("Login:")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 7])
    with col1:
        if st.button("Log in!"):
            if login and password:
                try:
                    response = requests.post(f"{base_url}login_user/", json = {"username": login, "password": password})

                    if response.status_code == 200:
                        logged = response.json().get("logged", False)
                        if logged:
                            st.session_state.logged_in = True
                            st.success("Zalogowano pomyślnie!")
                            st.session_state.user = User(login)
                            st.rerun()
                        else:
                            st.warning("Logowanie nie powiodło się: nieprawidłowe dane!")
                    else:
                        st.error(f"Logowanie nie powiodło się: {response.json().get('message', 'Nieznany błąd')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Wystąpił błąd połączenia z serwerem: {e}")
            else:
                st.warning("Proszę wypełnić wszystkie pola!")

    with col2:
        if st.button("Register!"):
            if login and password:
                try:
                    response = requests.post(f"{base_url}register_user/", json = {"username": login, "password": password})

                    if response.status_code == 200:
                        st.success("Użytkownik został zarejestrowany!")
                    else:
                        st.error(f"Rejestracja nie powiodła się: {response.json().get('message', 'Nieznany błąd')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Wystąpił błąd połączenia z serwerem: {e}")
            else:
                st.warning("Proszę wypełnić wszystkie pola!")
else:
    st.header(f"Hi, {st.session_state.user.username}! You are logged in!")
    if st.button("Log out", type="primary"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.write("You have been logged out!")
        st.rerun()
