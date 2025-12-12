"""
Modales d'édition.
"""
import streamlit as st
from components.forms import RouteForm, AttemptForm

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

@st.dialog("Confirmer la suppression")
def confirm_delete_dialog(item_name, on_confirm):
    """
    Modal de confirmation de suppression.
    
    Args:
        item_name: nom de l'élément à supprimer
        on_confirm: callback() appelé si l'utilisateur confirme
    """
    st.warning(f"Es-tu sûr de vouloir supprimer **{item_name}** ?")
    st.markdown("Cette action est **irréversible**.")

    if st.button("Supprimer", use_container_width=True, type="primary"):
        on_confirm()
        st.rerun()

    if st.button("Annuler", use_container_width=True, type="secondary"):
        st.rerun()
    
