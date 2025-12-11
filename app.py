import streamlit as st

# config de base
st.set_page_config(
    page_title="Climbing Tracker",
    page_icon="🧗",
    layout="wide"
)

st.header("Header",anchor=False, divider="orange", text_alignment="center",width="content")

# définition des pages
pages = [
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊"),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯")
]

current = st.navigation(pages,position="top")
current.run()
