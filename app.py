import streamlit as st
from services.auth_service import AuthService
from services.session_state_service import SessionStateService
from components.side_bar_menu import display_sidebar_menu, display_top_menu

# ----------------------
# Config de base
# ----------------------
st.set_page_config(
    page_title="Climbing Tracker",
    page_icon="🧗",
    layout="wide"
)

# Initialiser l'état global de l'app (auth, etc.)
SessionStateService.init_app_state()

# Vérifier la session
AuthService.check_session()

st.header("⛰️ Climbing tracker", anchor=False, divider="orange", text_alignment="center", width="content")

# ----------------------
# Définition des pages
# ----------------------
pages = [
    st.Page("pages/login_page.py", title="Connexion", icon="🔐"),
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊", default=True),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯"),
    st.Page("pages/route_detail_page.py", title="Détail voie", icon="🔍")
]
# Afficher le top menu personnalisé
display_top_menu()

current = st.navigation(pages, position="hidden")  # Permet à st.switch_page de fonctionner
current.run()

# Afficher le menu latéral personnalisé
display_sidebar_menu()