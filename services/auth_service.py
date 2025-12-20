"""
Service d'authentification avec Supabase Auth.
"""
import streamlit as st
from data.supabase_client import supabase

class AuthService:
    """Gestion de l'authentification utilisateur"""
       
    @staticmethod
    def sign_up(email, password):
        """
        Inscription d'un nouvel utilisateur.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                return True, "✅ Compte créé ! Vérifie ton email pour confirmer ton compte."
            else:
                return False, "❌ Erreur lors de la création du compte."
        except Exception as e:
            return False, f"❌ Erreur : {str(e)}"
    
    @staticmethod
    def sign_in(email, password):
        """
        Connexion d'un utilisateur.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                st.session_state.user = response.user
                st.session_state.session = response.session
                return True, "✅ Connexion réussie !"
            else:
                return False, "❌ Email ou mot de passe incorrect."
        except Exception as e:
            return False, f"❌ Erreur : {str(e)}"
    
    @staticmethod
    def sign_out():
        """Déconnexion de l'utilisateur"""
        try:
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.session = None
            return True, "👋 Déconnexion réussie."
        except Exception as e:
            return False, f"❌ Erreur lors de la déconnexion : {str(e)}"
    
    @staticmethod
    def get_current_user():
        """
        Récupère l'utilisateur actuellement connecté.
        
        Returns:
            User object ou None
        """
        return st.session_state.get("user", None)
    
    @staticmethod
    def get_user_id():
        """
        Récupère l'ID de l'utilisateur connecté.
        
        Returns:
            str: user_id ou None
        """
        user = AuthService.get_current_user()
        return user.id if user else None
    
    @staticmethod
    def is_authenticated():
        """Vérifie si un utilisateur est connecté"""
        return st.session_state.get("user") is not None
    
    @staticmethod
    def require_auth():
        """
        Vérifie l'authentification et redirige vers login si nécessaire.
        À utiliser au début de chaque page protégée.
        """
        if not AuthService.is_authenticated():
            st.warning("🔒 Tu dois te connecter pour accéder à cette page.")
            st.switch_page("pages/login_page.py")
            st.stop()
    
    @staticmethod
    def check_session():
        """
        Vérifie la validité de la session et la rafraîchit si nécessaire.
        """
        try:
            session = st.session_state.get("session")
            if session:
                # Vérifier si la session est toujours valide
                response = supabase.auth.get_user(session.access_token)
                if response.user:
                    st.session_state.user = response.user
                    return True
            return False
        except Exception:
            # Session expirée ou invalide
            st.session_state.user = None
            st.session_state.session = None
            return False