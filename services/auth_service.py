"""
Service d'authentification avec Supabase Auth.
"""
import streamlit as st
from data.supabase_client import supabase
from services.user_context import UserContext
from services.cookie_manager import CookieManager

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
                # Stocker dans session_state
                st.session_state.user = response.user
                st.session_state.session = response.session
                
                # Stocker dans les cookies pour persistance
                CookieManager.save_session(
                    response.session.access_token,
                    response.session.refresh_token
                )
                
                # Configurer Supabase avec la session
                supabase.auth.set_session(
                    response.session.access_token,
                    response.session.refresh_token
                )
                
                return True, "✅ Connexion réussie !"
            else:
                return False, "❌ Email ou mot de passe incorrect."
        except Exception as e:
            return False, f"❌ Erreur : {str(e)}"
    
    @staticmethod
    def sign_out():
        """Déconnexion de l'utilisateur.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.session = None
            CookieManager.clear_session()
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
        return UserContext.get_user()
    
    @staticmethod
    def get_user_id():
        """
        Récupère l'ID de l'utilisateur connecté.
        
        Returns:
            str: user_id ou None
        """
        return UserContext.get_user_id()
    
    @staticmethod
    def is_authenticated():
        """Vérifie si un utilisateur est connecté"""
        return UserContext.is_authenticated()
    
    @staticmethod
    def require_auth():
        """
        Vérifie l'authentification et redirige vers login si nécessaire.
        À utiliser au début de chaque page protégée.
        """
        if not UserContext.is_authenticated():
            st.switch_page("pages/login_page.py")
            st.stop()
    
    @staticmethod
    def restore_session_from_cookie():
        """
        Restaure la session depuis les cookies au démarrage de l'app.
        À appeler au début de app.py
        
        Returns:
            bool: True si la session a été restaurée avec succès
        """
        # Si déjà connecté dans session_state, pas besoin de restaurer
        if st.session_state.get("user") is not None:
            return True
        
        # Récupérer les tokens depuis les cookies
        session_data = CookieManager.get_session()
        
        if not session_data:
            return False
        
        try:
            # Tenter de restaurer la session avec les tokens
            access_token = session_data.get("access_token")
            refresh_token = session_data.get("refresh_token")
            
            if not access_token or not refresh_token:
                return False
            
            # Configurer Supabase avec les tokens
            supabase.auth.set_session(access_token, refresh_token)
            
            # Récupérer l'utilisateur avec le token
            response = supabase.auth.get_user(access_token)
            
            if response.user:
                # Restaurer dans session_state
                st.session_state.user = response.user
                
                # Récupérer la nouvelle session (peut avoir été rafraîchie)
                current_session = supabase.auth.get_session()
                if current_session:
                    st.session_state.session = current_session
                    
                    # Mettre à jour les cookies avec les tokens potentiellement rafraîchis
                    CookieManager.save_session(
                        current_session.access_token,
                        current_session.refresh_token
                    )
                
                return True
            else:
                # Token invalide, nettoyer
                CookieManager.clear_session()
                return False
                
        except Exception as e:
            # En cas d'erreur, nettoyer les cookies invalides
            CookieManager.clear_session()
            st.session_state.user = None
            st.session_state.session = None
            return False
    
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
                    supabase.auth.set_session(
                        session.access_token,
                        session.refresh_token
                    )
                    return True
            return False
        except Exception:
            # Session expirée ou invalide
            st.session_state.user = None
            st.session_state.session = None
            CookieManager.clear_session()
            return False