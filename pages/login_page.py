"""
Page de connexion et inscription.
"""
import streamlit as st
from services.auth_service import AuthService
from services.session_state_service import SessionStateService

# Initialiser l'état d'authentification
SessionStateService.init_app_state()

st.subheader("🔐 Connexion")

# Si déjà connecté, rediriger
if AuthService.is_authenticated():
    st.success("✅ Tu es déjà connecté !")
    if st.button("Aller au tableau de bord", use_container_width=True):
        st.switch_page("pages/dashboard_page.py")
    st.stop()

# Onglets connexion / inscription
tab1, tab2 = st.tabs(["Se connecter", "S'inscrire"])

with tab1:
    st.markdown("### Connexion")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="ton@email.com")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
        
        if submit:
            if not email or not password:
                st.error("❌ Remplis tous les champs.")
            else:
                success, message = AuthService.sign_in(email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

with tab2:
    st.markdown("### Créer un compte")
    
    with st.form("signup_form"):
        email = st.text_input("Email", placeholder="ton@email.com", key="signup_email")
        password = st.text_input("Mot de passe", type="password", key="signup_password", help="Minimum 6 caractères")
        password_confirm = st.text_input("Confirmer le mot de passe", type="password", key="signup_password_confirm")
        submit = st.form_submit_button("Créer mon compte", use_container_width=True, type="primary")
        
        if submit:
            errors = []
            
            if not email or not password or not password_confirm:
                errors.append("Remplis tous les champs.")
            
            if len(password) < 6:
                errors.append("Le mot de passe doit contenir au moins 6 caractères.")
            
            if password != password_confirm:
                errors.append("Les mots de passe ne correspondent pas.")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                success, message = AuthService.sign_up(email, password)
                if success:
                    st.success(message)
                    st.info("💡 Après confirmation, reviens sur cette page pour te connecter.")
                else:
                    st.error(message)