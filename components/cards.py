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
        
        display = f"{color_emoji} **{route['grade']}** — {route['name']}"
        if archived:
            display += " — 🔒 _Archivée_"
        
        if archived:
            # Pour les voies archivées : bouton réactiver
            col_data, col_edit, col_unarchive = st.columns([8, 1, 1])
        else:
            # Pour les voies actives : boutons éditer et archiver
            col_data, col_edit, col_archive = st.columns([8, 1, 1])
        
        with col_data:
            st.markdown(display)
        
        with col_edit:
            if on_edit:
                btn_key = f"route_{route.get('id')}_edit"
                if st.button("", key=btn_key, icon="✏️"):
                    on_edit()
        
        if archived:
            with col_unarchive:
                if on_unarchive:
                    btn_key = f"route_{route.get('id')}_unarchive"
                    if st.button("", key=btn_key, icon="♻️", help="Réactiver"):
                        on_unarchive()
        else:
            with col_archive:
                if on_archive:
                    btn_key = f"route_{route.get('id')}_archive"
                    if st.button("", key=btn_key, icon="🗑️", help="Archiver"):
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
        status = "✅ Réussie" if attempt.get("success") else "❌ Échouée"
        
        # Notes
        notes = attempt.get("notes")
        notes_display = f" — *{notes}*" if notes and notes.strip() else ""
        
        col_data, col_edit, col_del = st.columns([8, 1, 1])
        
        with col_data:
            st.markdown(
                f"{date_str} — {route_color} **{route_grade} {route_name}** — {status}{notes_display}"
            )
        
        with col_edit:
            if on_edit:
                btn_key = f"attempt_{attempt.get('id')}_edit"
                if st.button("", key=btn_key, icon="✏️"):
                    on_edit()
        
        with col_del:
            if on_delete:
                btn_key = f"attempt_{attempt.get('id')}_del"
                if st.button("", key=btn_key, icon="🗑️"):
                    on_delete()