import streamlit as st
from services.auth_service import AuthService
from services.session_state_service import SessionStateService


# config de base
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

# définition des pages
pages = [
    st.Page("pages/login_page.py", title="Connexion", icon="🔐"),
    st.Page("pages/dashboard_page.py", title="Tableau de bord", icon="📊"),
    st.Page("pages/routes_page.py", title="Voies", icon="🧗"),
    st.Page("pages/attempts_page.py", title="Tentatives", icon="🎯"),
    st.Page("pages/route_detail_page.py", title="Détail voie", icon="🔍")
]

# Navigation conditionnelle selon l'état de connexion
if AuthService.is_authenticated():
    current = st.navigation(pages, position="hidden")
    
    with st.container(horizontal=True, gap="small", vertical_alignment="center"):
        st.page_link("pages/dashboard_page.py", label="Dashboard", icon="📊")
        st.page_link("pages/routes_page.py", label="Voies", icon="🧗")
        st.page_link("pages/attempts_page.py", label="Tentatives", icon="🎯")
        
        # Bouton déconnexion
        user = AuthService.get_current_user()
        user_email = user.email if user else "Utilisateur"
        
        with st.popover(f"👤 {user_email}", use_container_width=False):
            st.markdown(f"**Connecté en tant que :**  \n{user_email}")
            if st.button("Se déconnecter", use_container_width=True, type="secondary"):
                success, message = AuthService.sign_out()
                if success:
                    st.rerun()
else:
    # Si non connecté, afficher seulement la page de login
    current = st.navigation([pages[0]], position="hidden")

current.run()