"""
Composants de filtrage réutilisables.
"""
import streamlit as st
from utils.constants import ROUTE_COLORS, GRADES, ROUTE_SPACES

class FilterComponents:
    """Composants UI pour les filtres"""
    
    @staticmethod
    def period_filter():
        """Filtre de sélection de période"""

        period_options = ["Aujourd'hui", "Semaine", "Mois", "Tout"]
        
        # Mapping session_state → label
        current_map = {
            "Aujourd'hui": "Aujourd'hui",
            "Cette semaine": "Semaine",
            "Ce mois-ci": "Mois",
            "Tout": "Tout"
        }
        current_period = current_map.get(st.session_state.filter_period, "Tout")
        
        selected = st.segmented_control(
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
    def status_filter():
        """Filtre de sélection de statut"""
        
        status_options = ["Toutes", "✅ Réussies", "❌ Échouées"]
        
        # Mapping session_state → label
        current_map = {
            "Toutes": "Toutes",
            "Réussies": "✅ Réussies",
            "Échouées": "❌ Échouées"
        }
        current_status = current_map[st.session_state.filter_status]
        
        selected = st.segmented_control(
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
    def colors_multiselect():
        """Multiselect pour filtrer par couleurs"""
        selected_colors = st.multiselect(
            "Filtrer par couleurs",
            options=list(ROUTE_COLORS.keys()),
            default=st.session_state.filter_colors,
            format_func=lambda c: f"{ROUTE_COLORS[c]} {c}",
            placeholder="Toutes les couleurs"
        )
        
        # Comparer et rerun si changement
        if selected_colors != st.session_state.filter_colors:
            st.session_state.filter_colors = selected_colors
            st.rerun()

    @staticmethod
    def grades_range_slider():
        """Slider pour filtrer par plage de cotations"""
        min_grade, max_grade = st.select_slider(
            "Plage de cotations",
            options=GRADES,
            value=(
                st.session_state.filter_min_grade,
                st.session_state.filter_max_grade
            )
        )
        if (min_grade != st.session_state.filter_min_grade or
            max_grade != st.session_state.filter_max_grade):
            st.session_state.filter_min_grade = min_grade
            st.session_state.filter_max_grade = max_grade
            st.rerun()


    @staticmethod
    def space_select():
        """Select pour filtrer par zone"""
        selected_space = st.pills(
            "Filtrer par zone",
            options=list(ROUTE_SPACES),
            default=st.session_state.filter_space
        )
        
        # Comparer et rerun si changement
        if selected_space != st.session_state.filter_space:
            st.session_state.filter_space = selected_space
            st.rerun()