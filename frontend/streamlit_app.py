import streamlit as st

pages = {
    "Your account": [
        st.Page("login_page.py", title="Log into account"),
        st.Page("id_page.py", title="Check your id"),
    ],
    "Find A Time": [
        st.Page("home_page.py", title="Add a spot"),
        st.Page("find_a_time_page.py", title="Try it out"),
        st.Page("add_group_page.py", title="Manage your group"),
    ],
}

pg = st.navigation(pages)
pg.run()