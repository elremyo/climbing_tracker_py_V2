import streamlit as st
from services.auth_service import AuthService
from streamlit_extras.skeleton import skeleton

# ----------------------
# Sidebar navigation customisée
# ----------------------

def display_sidebar_menu():
    # Show a navigation menu in the sidebar
    with st.sidebar:
        if AuthService.is_authenticated():
            # Liens vers les pages visibles
            st.sidebar.page_link("pages/dashboard_page.py", label="Dashboard", icon="📊")
            st.sidebar.page_link("pages/routes_page.py", label="Voies", icon="🧗")
            st.sidebar.page_link("pages/attempts_page.py", label="Tentatives", icon="🎯")

            # Popover profil + déconnexion
            user = AuthService.get_current_user()
            user_email = user.email if user else "Utilisateur"
            with st.expander(f"Mon compte", expanded=False, icon="👤"):
                st.markdown(f"**Connecté en tant que :**  \n{user_email}")
                if st.button("Se déconnecter", use_container_width=True, type="secondary"):
                    success, message = AuthService.sign_out()
                    if success:
                        st.success(message)
                        st.switch_page("pages/login_page.py")
        else:
            # Si non connecté, afficher juste un lien vers login
            st.sidebar.page_link("pages/login_page.py", label="Se connecter", icon="🔐")

def display_top_menu():
    if not st.runtime.exists():
        skeleton()
        return

    try:
        with st.container(horizontal=True):
            st.page_link("pages/dashboard_page.py", label="", icon="📊")
            st.page_link("pages/routes_page.py", label="", icon="🧗")
            st.page_link("pages/attempts_page.py", label="", icon="🎯")
    except KeyError:
        skeleton()