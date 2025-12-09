import streamlit as st
from pathlib import Path

# config de base
st.set_page_config(page_title="Climbing Tracker", layout="wide")

# définition des pages
pages = [
    st.Page("pages/home.py", title="Accueil", icon="🏠"),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯"),
]

current = st.navigation(pages,position="top")
current.run()
