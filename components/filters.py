"""
Composants de filtrage réutilisables.
"""
import streamlit as st
from utils.constants import ROUTE_COLORS, GRADES

class FilterComponents:
    """Composants UI pour les filtres"""
    
    @staticmethod
    def period_pills():
        """Pills de sélection de période"""

        period_options = ["Aujourd'hui", "Semaine", "Mois", "Tout"]
        
        # Mapping session_state → label
        current_map = {
            "Aujourd'hui": "Aujourd'hui",
            "Cette semaine": "Semaine",
            "Ce mois-ci": "Mois",
            "Tout": "Tout"
        }
        current_period = current_map.get(st.session_state.filter_period, "Tout")
        
        selected = st.pills(
            "Période",
            options=period_options,
            selection_mode="single",
            default=current_period
            )
        
        # Mapping label → session_state
        reverse_map = {
            "Aujourd'hui": "Aujourd'hui",
            "Semaine": "Cette semaine",
            "Mois": "Ce mois-ci",
            "Tout": "Tout"
        }
        new_period = reverse_map[selected]
        
        if new_period != st.session_state.filter_period:
            st.session_state.filter_period = new_period
            st.rerun()
    
    @staticmethod
    def status_pills():
        """Pills de sélection de statut"""
        
        status_options = ["Toutes", "✅ Réussies", "❌ Échouées"]
        
        # Mapping session_state → label
        current_map = {
            "Toutes": "Toutes",
            "Réussies": "✅ Réussies",
            "Échouées": "❌ Échouées"
        }
        current_status = current_map[st.session_state.filter_status]
        
        selected = st.pills(
            "Statut",
            options=status_options,
            selection_mode="single",
            default=current_status
        )
        
        # Mapping label → session_state
        reverse_map = {
            "Toutes": "Toutes",
            "✅ Réussies": "Réussies",
            "❌ Échouées": "Échouées"
        }
        new_status = reverse_map[selected]
        
        if new_status != st.session_state.filter_status:
            st.session_state.filter_status = new_status
            st.rerun()
    
    @staticmethod
    def routes_multiselect(routes):
        """Multiselect pour filtrer par voies"""
        if not routes:
            return
        
        route_options = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
        selected_routes = st.multiselect(
            "Filtrer par voies",
            options=list(route_options.keys()),
            default=[k for k, v in route_options.items() if v in st.session_state.filter_routes],
            placeholder="Sélectionne une ou plusieurs voies"
        )
        st.session_state.filter_routes = [route_options[r] for r in selected_routes]
    
    @staticmethod
    def colors_multiselect():
        """Multiselect pour filtrer par couleurs"""
        selected_colors = st.multiselect(
            "Filtrer par couleurs",
            options=list(ROUTE_COLORS.keys()),
            default=st.session_state.filter_colors,
            format_func=lambda c: f"{ROUTE_COLORS[c]} {c}",
            placeholder="Toutes les couleurs"
        )
        st.session_state.filter_colors = selected_colors
    
    @staticmethod
    def grades_multiselect():
        """Multiselect pour filtrer par cotations"""
        selected_grades = st.multiselect(
            "Filtrer par cotations",
            options=GRADES,
            default=st.session_state.filter_grades,
            placeholder="Toutes les cotations"
        )
        st.session_state.filter_grades = selected_grades