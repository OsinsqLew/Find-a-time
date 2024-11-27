import streamlit as st

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    pages = {
    "Your account": [
        st.Page("login_page.py", title="Account"),
        # st.Page("id_page.py", title="Check your id"),
    ]}
else:
    pages = {
        "Your account": [
            st.Page("login_page.py", title="Account"),
            # st.Page("id_page.py", title="Check your id"),
        ],
        "Find A Time": [
            st.Page("add_spot_page.py", title="Add a spot"),
            st.Page("find_a_time_page.py", title="Find a time"),
            st.Page("add_group_page.py", title="Manage your group"),
        ],
        "Additional":[
            st.Page("sql_injection.py", title="SQL Injection Demo"),
        ],
    }

pg = st.navigation(pages)
pg.run()