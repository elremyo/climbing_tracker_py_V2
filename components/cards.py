"""
Composants d'affichage pour routes et attempts.
"""
import streamlit as st
from utils.constants import ROUTE_COLORS
from utils.formatting import format_date_fr

class RouteCard:
    """Affichage d'une voie"""
    
    @staticmethod
    def render(route, on_edit=None, on_archive=None, on_unarchive=None):
        """
        Affiche une carte de voie.
        
        Args:
            route: dict de la voie
            on_edit: callback() appelé au clic sur éditer
            on_archive: callback() appelé au clic sur archiver
            on_unarchive: callback() appelé au clic sur réactiver
        """
        color_emoji = ROUTE_COLORS.get(route["color"], "❓")
        archived = route.get("archived", False)
        route_type = route.get("type")
        type_badge = f" :violet-badge[{route_type}]" if route_type else ""
        
        display = f"{color_emoji} **{route['grade']}** - :small[{route['name']}{type_badge}]"
        if archived:
            display = f''':grey[{display + " - :material/lock: _Archivée_"}]''' 

        with st.container(horizontal=True,border=True,vertical_alignment="center"):
            st.markdown(display)
            if on_edit:
                btn_key = f"route_{route.get('id')}_edit"
                if st.button("", key=btn_key, icon=":material/edit:", help="Éditer",type="tertiary"):
                    on_edit()
            if archived:
                if on_unarchive:
                    btn_key = f"route_{route.get('id')}_unarchive"
                    if st.button("", key=btn_key, icon=":material/lock_reset:", help="Réactiver",type="tertiary"):
                        on_unarchive()
            else:
                if on_archive:
                    btn_key = f"route_{route.get('id')}_archive"
                    if st.button("", key=btn_key, icon=":material/archive:", help="Archiver",type="tertiary"):
                        on_archive()

class AttemptCard:
    """Affichage d'une tentative"""
    
    @staticmethod
    def render(attempt, route, on_edit=None, on_delete=None):
        """
        Affiche une carte de tentative.
        
        Args:
            attempt: dict de la tentative
            route: dict de la voie (ou None si supprimée)
            on_edit: callback() appelé au clic sur éditer
            on_delete: callback() appelé au clic sur supprimer
        """
        # Infos de la voie
        if route:
            route_name = route["name"]
            route_color = ROUTE_COLORS.get(route["color"], "❓")
            route_grade = route["grade"]
        else:
            route_name = "Voie supprimée"
            route_color = "❓"
            route_grade = ""
        
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
        
        
        with st.container(horizontal=True,border=True,vertical_alignment="center"):
            with st.container():
                st.markdown(f"{date_str} - {route_color} **{route_grade} {route_name}**")
                st.markdown(f"{status}")
                st.markdown(f":small[{notes_display}]")
            if on_edit:
                btn_key = f"attempt_{attempt.get('id')}_edit"
                if st.button("", key=btn_key, icon=":material/edit:", help="Éditer",type="tertiary"):
                    on_edit()

            if on_delete:
                btn_key = f"attempt_{attempt.get('id')}_del"
                if st.button("", key=btn_key, icon=":material/delete:", help="Supprimer",type="tertiary"):
                    on_delete()