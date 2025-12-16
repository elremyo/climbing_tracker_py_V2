import streamlit as st

# config de base
st.set_page_config(
    page_title="Climbing Tracker",
    page_icon="🧗",
    layout="centered"
)

st.header("⛰️ Climbing tracker",anchor=False, divider="orange", text_alignment="center",width="content")

# définition des pages
pages = [
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon=":material/analytics:"),
    st.Page("pages/routes_page.py", title="Voies", icon=":material/tools_ladder:"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon=":material/target:"),
    st.Page("pages/route_detail_page.py", title="Détail voie", icon=":material/search:")

]

current = st.navigation(pages,position="hidden")

with st.container(horizontal=True,gap="small", vertical_alignment="center"):
    st.page_link("pages/dashboard_page.py", label="Dashboard", icon=":material/analytics:")
    st.page_link("pages/routes_page.py", label="Voies", icon=":material/tools_ladder:")
    st.page_link("pages/attempts_page.py", label="Tentatives", icon=":material/target:")


current.run()