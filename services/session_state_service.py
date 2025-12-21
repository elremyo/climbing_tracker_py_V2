"""
Gestion centralisée du session_state.
"""
import streamlit as st
from utils.constants import GRADES

class SessionStateService:
    """Service de gestion du session_state"""
    
    @staticmethod
    def init_app_state():
        """Initialize global app state (auth, etc.)"""
        defaults = {
            "user": None,
            "session": None,
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value


    @staticmethod
    def init_routes_state():
        """Initialize routes page state"""
        defaults = {
            "show_add_success": False,
            "show_edit_success": False,
            "show_delete_success": False,
            "filter_colors": [],
            "filter_min_grade": GRADES[0],
            "filter_max_grade": GRADES[-1],
            "filter_space": [],
            "sort_by": "Cotation",  # Options: "Cotation", "Relais", "Tentatives"
            "sort_direction": "Décroissant"  # Options: "Croissant", "Décroissant"
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def init_attempts_state():
        """Initialize attempts page state"""
        defaults = {
            "show_attempt_add_success": False,
            "show_attempt_edit_success": False,
            "show_attempt_delete_success": False,
            "filter_period": "Tout",
            "filter_status": "Toutes",
            "filter_routes": [],
            "sort_order": "Plus récent",
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def reset_routes_filters():
        """Reset all routes filters"""
        st.session_state.filter_colors = []
        st.session_state.filter_space = []
        st.session_state.filter_min_grade = GRADES[0]
        st.session_state.filter_max_grade = GRADES[-1]
        st.session_state.sort_by = "Cotation"
        st.session_state.sort_direction = "Décroissant"
    
    @staticmethod
    def reset_attempts_filters():
        """Reset all attempts filters"""
        st.session_state.filter_period = "Tout"
        st.session_state.filter_status = "Toutes"
        st.session_state.sort_order = "Plus récent"