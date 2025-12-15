import streamlit as st

# config de base
st.set_page_config(
    page_title="Climbing Tracker",
    page_icon="🧗",
    layout="wide"
)

st.header("⛰️ Climbing tracker",anchor=False, divider="orange", text_alignment="center",width="content")

# définition des pages
pages = [
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊"),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯"),
    st.Page("pages/route_detail_page.py", title="Détail voie", icon="🔍")

]

current = st.navigation(pages,position="hidden")

with st.container(horizontal=True,gap="small", vertical_alignment="center"):
    st.page_link("pages/dashboard_page.py", label="Dashboard", icon="📊")
    st.page_link("pages/routes_page.py", label="Voies", icon="🧗")
    st.page_link("pages/attempts_page.py", label="Tentatives", icon="🎯")


current.run()