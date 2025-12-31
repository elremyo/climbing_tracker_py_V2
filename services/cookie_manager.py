"""
Gestionnaire de cookies avec chiffrement pour sécuriser sur domaines partagés.
"""
import extra_streamlit_components as stx
import json
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class SecureCookieManager:
    """Gestion des cookies avec chiffrement"""
    
    _cookie_manager = None
    COOKIE_NAME = "climbing_tracker_session"
    
    # Clé de chiffrement (à mettre dans .env !)
    # Générer avec : Fernet.generate_key().decode()
    ENCRYPTION_KEY = os.environ.get("COOKIE_ENCRYPTION_KEY")
    
    @classmethod
    def _get_cipher(cls):
        """Récupère le cipher pour chiffrer/déchiffrer"""
        if not cls.ENCRYPTION_KEY:
            raise ValueError("COOKIE_ENCRYPTION_KEY non trouvé dans .env")
        return Fernet(cls.ENCRYPTION_KEY.encode())
    
    @classmethod
    def get_manager(cls):
        """Récupère ou crée l'instance du cookie manager"""
        if cls._cookie_manager is None:
            cls._cookie_manager = stx.CookieManager()
        return cls._cookie_manager
    
    @classmethod
    def save_session(cls, access_token, refresh_token):
        """
        Sauvegarde les tokens chiffrés dans un cookie.
        """
        manager = cls.get_manager()
        cipher = cls._get_cipher()
        
        session_data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
        # Chiffrer les données
        json_data = json.dumps(session_data)
        encrypted_data = cipher.encrypt(json_data.encode()).decode()
        
        # Sauvegarder le cookie chiffré
        manager.set(
            cls.COOKIE_NAME,
            encrypted_data,
            expires_at=None,
            key="save_session"
        )
    
    @classmethod
    def get_session(cls):
        """
        Récupère et déchiffre les tokens depuis le cookie.
        
        Returns:
            dict: {"access_token": str, "refresh_token": str} ou None
        """
        manager = cls.get_manager()
        cipher = cls._get_cipher()
        
        encrypted_value = manager.get(cls.COOKIE_NAME)
        
        if encrypted_value:
            try:
                # Déchiffrer
                decrypted_data = cipher.decrypt(encrypted_value.encode()).decode()
                return json.loads(decrypted_data)
            except Exception:
                # Cookie corrompu ou clé invalide
                return None
        return None
    
    @classmethod
    def clear_session(cls):
        """Supprime le cookie de session"""
        manager = cls.get_manager()
        manager.delete(cls.COOKIE_NAME, key="clear_session")