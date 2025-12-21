"""
Modales d'édition.
"""
import streamlit as st
from components.forms import RouteForm, AttemptForm

@st.dialog("Ajouter une voie")
def add_route_dialog(on_save):
    """
    Modal d'ajout de voie.
    
    Args:
        on_save: callback(name, grade, color) appelé lors de la sauvegarde
    """
    def handle_submit(name, grade, color):
        on_save(name, grade, color)
        st.rerun()
    
    def handle_cancel():
        st.rerun()

    RouteForm.render(on_submit=handle_submit, on_cancel=handle_cancel)


@st.dialog("Éditer la voie")
def edit_route_dialog(route, on_save):
    """
    Modal d'édition de voie.
    
    Args:
        route: dict de la voie à éditer
        on_save: callback(name, grade, color) appelé lors de la sauvegarde
    """
    def handle_submit(name, grade, color):
        on_save(name, grade, color)
        st.rerun()
    
    def handle_cancel():
        st.rerun()

    RouteForm.render(route=route, on_submit=handle_submit, on_cancel=handle_cancel)


@st.dialog("Ajouter une tentative")
def add_attempt_dialog(routes, on_save, fixed_route=None):
    """
    Modal d'ajout de tentative.
    
    Args:
        routes: liste des voies disponibles
        on_save: callback(route_id, success, notes, date) appelé lors de la sauvegarde
        fixed_route: dict de la voie fixe (si on ajoute depuis la page détail)
    """
    def handle_submit(route_id, success, notes, attempt_date):
        on_save(route_id, success, notes, attempt_date)
        st.rerun()
    
    def handle_cancel():
        st.rerun()

    AttemptForm.render(routes=routes, on_submit=handle_submit, on_cancel=handle_cancel, fixed_route=fixed_route)


@st.dialog("Éditer la tentative")
def edit_attempt_dialog(attempt, routes, on_save):
    """
    Modal d'édition de tentative.
    
    Args:
        attempt: dict de la tentative à éditer
        routes: liste des voies disponibles
        on_save: callback(route_id, success, notes, date) lors de la sauvegarde
    """
    def handle_submit(route_id, success, notes, attempt_date):
        on_save(route_id, success, notes, attempt_date)
        st.rerun()
    
    def handle_cancel():
        st.rerun()

    AttemptForm.render(routes=routes, attempt=attempt, on_submit=handle_submit, on_cancel=handle_cancel)

@st.dialog("Confirmer l'archivage")
def confirm_archive_dialog(item_name, on_confirm):
    """
    Modal de confirmation de l'archivage.
    
    Args:
        item_name: nom de l'élément à archiver
        on_confirm: callback() appelé si l'utilisateur confirme
    """
    st.markdown(f"Es-tu sûr de vouloir archiver **{item_name}** ?")

    if st.button("Archiver", use_container_width=True, type="primary"):
        on_confirm()
        st.rerun()

    if st.button("Annuler", use_container_width=True, type="secondary"):
        st.rerun()