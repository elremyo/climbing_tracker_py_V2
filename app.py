import streamlit as st

# config de base
st.set_page_config(
    page_title="Climbing Tracker",
    page_icon="🧗",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.header("Header")

# définition des pages
pages = [
st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊"),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯")
]

current = st.navigation(pages,position="top")
current.run()
