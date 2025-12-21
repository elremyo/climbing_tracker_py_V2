"""
Composants d'affichage pour routes et attempts.
"""
import streamlit as st
from utils.constants import ROUTE_COLORS
from utils.formatting import format_date_fr

class RouteCard:
    """Affichage d'une voie"""
    
    @staticmethod
    def render(route, on_edit=None, on_click=None):
        """
        Affiche une carte de voie.
        
        Args:
            route: dict de la voie
            on_edit: callback() appelé au clic sur éditer
            on_click: callback() appelé au clic sur la carte (NOUVEAU)
        """
        color_emoji = ROUTE_COLORS.get(route["color"], "❓")
        
        display = f"{color_emoji} **{route['grade']}** - :small[{route['name']}]"

        with st.container(horizontal=True, border=True, vertical_alignment="center"):
            st.markdown(display,text_alignment="left")
            
            # Boutons d'actions
            if on_click:
                if st.button("", key=f"route_{route.get('id')}_click",icon=":material/search:", help="Détail",type="tertiary"):
                    on_click()

            if on_edit:
                btn_key = f"route_{route.get('id')}_edit"
                if st.button("", key=btn_key, icon=":material/edit:", help="Éditer", type="tertiary"):
                    on_edit()


class AttemptCard:
    """Affichage d'une tentative"""
    
    @staticmethod
    def render(attempt, route, on_edit=None, on_delete=None, show_route_info=True):
        """
        Affiche une carte de tentative.
        
        Args:
            attempt: dict de la tentative
            route: dict de la voie (ou None si supprimée)
            on_edit: callback() appelé au clic sur éditer
            on_delete: callback() appelé au clic sur supprimer
            show_route_info: bool, afficher les infos de la voie (défaut: True)

        """
        # Infos de la voie
        if show_route_info:
            if route:
                route_name = route["name"]
                route_color = ROUTE_COLORS.get(route["color"], "❓")
                route_grade = route["grade"]
                route_display = f"{route_color} **{route_grade} {route_name}**"
            else:
                route_display = "❓ **Voie supprimée**"
        else:
            route_display = None
        
        # Format date
        date_str = format_date_fr(attempt["date"])
        
        # Status
        if attempt.get("success"):
            status = ":green-badge[:material/check: Réussie]"
        else:
            status = ":red-badge[:material/close: Échouée]"        
        
        # Notes
        notes = attempt.get("notes")
        if notes and notes.strip():
            notes = notes.strip()
        notes_display = f"*{notes}*" if notes and notes.strip() else ""
        
        with st.container(horizontal=True, border=True, vertical_alignment="center"):
            with st.container():

                if route_display:
                    st.markdown(f"{date_str} - {route_display}")
                else:
                    st.markdown(f"**{date_str}**")
                st.markdown(f"{status}")
                st.markdown(f":small[{notes_display}]")
            
            if on_edit:
                btn_key = f"attempt_{attempt.get('id')}_edit"
                if st.button("", key=btn_key, icon=":material/edit:", help="Éditer", type="tertiary"):
                    on_edit()

            if on_delete:
                btn_key = f"attempt_{attempt.get('id')}_del"
                if st.button("", key=btn_key, icon=":material/delete:", help="Supprimer", type="tertiary"):
                    on_delete()