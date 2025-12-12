import streamlit as st
from data import get_routes, get_attempts, add_attempt, update_attempt, delete_attempt
from services.session_state_service import SessionStateService
from services.filter_service import FilterService
from components.filters import FilterComponents
from components.forms import AttemptForm
from components.cards import AttemptCard
from components.dialogs import edit_attempt_dialog

# Style CSS
st.markdown("""
    <style>
        div[data-testid="stColumn"] {
            width: fit-content !important;
            flex: unset;
        }
        div[data-testid="stColumn"] * {
            width: fit-content !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialisation
SessionStateService.init_attempts_state()

# Chargement des données
attempts = get_attempts()
routes = get_routes()
filtered_attempts = FilterService.filter_attempts(attempts, routes)

# Header
st.subheader(f"🎯 Mes tentatives ({len(filtered_attempts)}/{len(attempts)})")

# Bouton ajouter
if st.button("➕ Ajouter une tentative", key="add_attempt_button", use_container_width=True):
    st.session_state.show_attempt_form = True

# Filtres rapides
FilterComponents.period_pills()
FilterComponents.status_pills()

# Filtres avancés
with st.expander("🔍 Filtres avancés"):
    FilterComponents.routes_multiselect(routes)
    
    sort_option = st.radio(
        "Trier par",
        ["Plus récent", "Plus ancien"],
        index=0 if st.session_state.sort_order == "Plus récent" else 1,
        horizontal=True
    )
    if sort_option != st.session_state.sort_order:
        st.session_state.sort_order = sort_option
        st.rerun()
    
    if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
        SessionStateService.reset_attempts_filters()
        st.rerun()

st.divider()

# Formulaire d'ajout
if st.session_state.show_attempt_form:
    if not routes:
        st.warning("Ajoute d'abord une voie avant d'enregistrer une tentative.")
    else:
        def handle_submit(route_id, success, notes, attempt_date):
            add_attempt(route_id, success, notes, attempt_date)
            st.session_state.show_attempt_success = True
            st.session_state.show_attempt_form = False
            st.rerun()
        
        def handle_cancel():
            st.session_state.show_attempt_form = False
            st.rerun()
        
        AttemptForm.render(routes=routes, on_submit=handle_submit, on_cancel=handle_cancel)

# Liste des tentatives
if filtered_attempts:
    for a in filtered_attempts:
        route = next((r for r in routes if r['id'] == a['route_id']), None)
        
        def make_edit_handler(attempt, route_obj):
            def handler():
                def save_handler(route_id, success, notes, attempt_date):
                    update_attempt(attempt["id"], route_id, success, notes, attempt_date)
                    st.toast("✅ Tentative modifiée !", icon="✅")
                edit_attempt_dialog(attempt, routes, save_handler)
            return handler
        
        def make_delete_handler(attempt, route_obj):
            def handler():
                # Import de la fonction de confirmation
                from components.dialogs import confirm_delete_dialog
                
                # Créer le nom d'affichage pour la modale
                if route_obj:
                    display_name = f"{route_obj['grade']} {route_obj['name']}"
                else:
                    display_name = "cette tentative"
                
                # Callback de confirmation
                def on_confirm():
                    delete_attempt(attempt["id"])
                    st.toast("✅ Tentative supprimée !", icon="✅")
                
                confirm_delete_dialog(display_name, on_confirm)
            return handler
        
        AttemptCard.render(
            a,
            route,
            on_edit=make_edit_handler(a, route),
            on_delete=make_delete_handler(a, route)
        )
else:
    if attempts:
        st.info("Aucune tentative ne correspond aux filtres sélectionnés.")
    else:
        st.info("Aucune tentative enregistrée.")

# Message de succès
if st.session_state.show_attempt_success:
    st.toast("✅ Tentative enregistrée !", icon="✅")
    st.session_state.show_attempt_success = False