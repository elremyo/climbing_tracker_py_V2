import streamlit as st
from services.auth_service import AuthService
from services.session_state_service import SessionStateService

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
# route_detail_page est volontairement exclue du menu
pages = [
    st.Page("pages/login_page.py", title="Connexion", icon="🔐"),
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊", default=True),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯"),
    st.Page("pages/route_detail_page.py", title="Détail voie", icon="🔍")  # reste accessible via switch_page
]


# ----------------------
# Navigation top (optionnelle)
# ----------------------
current = st.navigation(pages, position="sidebar")  # Permet à st.switch_page de fonctionner
current.run()

# ----------------------
# Navigation sidebar
# ----------------------
with st.sidebar:
    if AuthService.is_authenticated():
        # Liens vers les pages visibles
        st.page_link("pages/dashboard_page.py", label="Dashboard", icon="📊")
        st.page_link("pages/routes_page.py", label="Voies", icon="🧗")
        st.page_link("pages/attempts_page.py", label="Tentatives", icon="🎯")
        
        # Popover profil + déconnexion
        user = AuthService.get_current_user()
        user_email = user.email if user else "Utilisateur"
        with st.expander(f"👤 Mon compte", expanded=False):
            st.markdown(f"**Connecté en tant que :**  \n{user_email}")
            if st.button("Se déconnecter", use_container_width=True, type="secondary"):
                success, message = AuthService.sign_out()
                if success:
                    st.switch_page("pages/login_page.py")
    else:
        # Si non connecté, afficher juste un lien vers login
        st.page_link("pages/login_page.py", label="Se connecter", icon="🔐")

with st.container(horizontal=True):
    st.page_link("pages/dashboard_page.py", label="", icon="📊")
    st.page_link("pages/routes_page.py", label="", icon="🧗")
    st.page_link("pages/attempts_page.py", label="", icon="🎯")