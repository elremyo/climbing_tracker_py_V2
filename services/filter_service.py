"""
Logique de filtrage et tri pour routes et attempts.
"""
from datetime import date, datetime, timedelta
from utils.constants import GRADES
import streamlit as st

class FilterService:
    """Service de filtrage des données"""
    
    @staticmethod
    def filter_routes(routes):
        """Applique les filtres aux voies"""
        filtered = routes.copy()
        
        # Filtre par couleurs
        if st.session_state.filter_colors:
            filtered = [r for r in filtered if r["color"] in st.session_state.filter_colors]
        
        # Filtre par plage de cotations (nouveau)
        min_idx = GRADES.index(st.session_state.filter_min_grade)
        max_idx = GRADES.index(st.session_state.filter_max_grade)
        filtered = [r for r in filtered 
                    if r["grade"] in GRADES[min_idx:max_idx+1]]
        return filtered
    
    @staticmethod
    def filter_attempts(attempts, routes):
        """Applique les filtres aux tentatives"""
        filtered = attempts.copy()
        
        # Filtre par période
        if st.session_state.filter_period != "Tout":
            today = date.today()
            
            if st.session_state.filter_period == "Aujourd'hui":
                date_limit = today
                filtered = [a for a in filtered if datetime.fromisoformat(a["date"]).date() == date_limit]
            
            elif st.session_state.filter_period == "Cette semaine":
                date_limit = today - timedelta(days=today.weekday())
                filtered = [a for a in filtered if datetime.fromisoformat(a["date"]).date() >= date_limit]
            
            elif st.session_state.filter_period == "Ce mois-ci":
                filtered = [a for a in filtered 
                           if datetime.fromisoformat(a["date"]).date().month == today.month 
                           and datetime.fromisoformat(a["date"]).date().year == today.year]
        
        # Filtre par statut
        if st.session_state.filter_status == "Réussies":
            filtered = [a for a in filtered if a.get("success")]
        elif st.session_state.filter_status == "Échouées":
            filtered = [a for a in filtered if not a.get("success")]
        
        # Tri
        if st.session_state.sort_order == "Plus récent":
            filtered = sorted(filtered, key=lambda a: a["date"], reverse=True)
        else:
            filtered = sorted(filtered, key=lambda a: a["date"], reverse=False)
        
        return filtered