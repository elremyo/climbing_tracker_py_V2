"""
Gestionnaire de cookies pour la persistance de session.
"""
import extra_streamlit_components as stx
import json

class CookieManager:
    """Gestion des cookies d'authentification"""
    
    _cookie_manager = None
    COOKIE_NAME = "climbing_tracker_session"
    
    @classmethod
    def get_manager(cls):
        """Récupère ou crée l'instance du cookie manager"""
        if cls._cookie_manager is None:
            cls._cookie_manager = stx.CookieManager()
        return cls._cookie_manager
    
    @classmethod
    def save_session(cls, access_token, refresh_token):
        """
        Sauvegarde les tokens de session dans un cookie.
        
        Args:
            access_token: token d'accès Supabase
            refresh_token: token de rafraîchissement Supabase
        """
        manager = cls.get_manager()
        session_data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        # Sauvegarder pour 30 jours
        manager.set(
            cls.COOKIE_NAME,
            json.dumps(session_data),
            expires_at=None,  # Persiste jusqu'à la fermeture du navigateur
            key="save_session"
        )
    
    @classmethod
    def get_session(cls):
        """
        Récupère les tokens de session depuis le cookie.
        
        Returns:
            dict: {"access_token": str, "refresh_token": str} ou None
        """
        manager = cls.get_manager()
        cookie_value = manager.get(cls.COOKIE_NAME)
        
        if cookie_value:
            try:
                return json.loads(cookie_value)
            except (json.JSONDecodeError, TypeError):
                return None
        return None
    
    @classmethod
    def clear_session(cls):
        """Supprime le cookie de session"""
        manager = cls.get_manager()
        manager.delete(cls.COOKIE_NAME, key="clear_session")