"""
Contexte utilisateur pour accès rapide à l'user_id sans circular import.
"""
import streamlit as st

class UserContext:
    """Gestion du contexte utilisateur courant"""
    
    @staticmethod
    def get_user_id():
        """
        Récupère l'ID de l'utilisateur connecté depuis session_state.
        
        Returns:
            str: user_id ou None
        """
        user = st.session_state.get("user", None)
        return user.id if user else None
    
    @staticmethod
    def get_user():
        """
        Récupère l'utilisateur connecté depuis session_state.
        
        Returns:
            User object ou None
        """
        return st.session_state.get("user", None)
    
    @staticmethod
    def is_authenticated():
        """Vérifie si un utilisateur est connecté"""
        return st.session_state.get("user") is not None
    

    