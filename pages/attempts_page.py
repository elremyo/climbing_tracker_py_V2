import streamlit as st
from data import get_routes, get_attempts, add_attempt, update_attempt, delete_attempt
from services.session_state_service import SessionStateService
from services.filter_service import FilterService
from components.filters import FilterComponents
from components.forms import AttemptForm
from components.cards import AttemptCard
from components.dialogs import add_attempt_dialog,edit_attempt_dialog

st.set_page_config(
    page_title="Tentatives"
)

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
st.subheader(f"Mes tentatives ({len(filtered_attempts)}/{len(attempts)})")

if st.button("Ajouter une tentative", key="add_attempt_button", icon=":material/add:", use_container_width=True, type="primary"):
    if not routes:
        st.warning("Ajoute d'abord une voie avant d'enregistrer une tentative.")
    else:
        def save_handler(route_id, success, notes, attempt_date):
            add_attempt(route_id, success, notes, attempt_date)
            st.session_state.show_attempt_add_success = True
        
        add_attempt_dialog(routes, save_handler)

# Filtres rapides
FilterComponents.status_filter()

# Filtres avancés
with st.expander("Filtres avancés"):
    FilterComponents.period_filter()
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
    
    if st.button("Réinitialiser les filtres", icon=":material/replay:",use_container_width=True):
        SessionStateService.reset_attempts_filters()
        st.rerun()

st.divider()

# Liste des tentatives
if filtered_attempts:
    for a in filtered_attempts:
        route = next((r for r in routes if r['id'] == a['route_id']), None)
        
        def make_edit_handler(attempt, route_obj):
            def handler():
                def save_handler(route_id, success, notes, attempt_date):
                    update_attempt(attempt["id"], route_id, success, notes, attempt_date)
                    st.session_state.show_attempt_edit_success = True
                edit_attempt_dialog(attempt, routes, save_handler)
            return handler
        
        def make_delete_handler(attempt, route_obj):
            def handler():
                # Import de la fonction de confirmation
                from components.dialogs import confirm_archive_dialog
                
                # Créer le nom d'affichage pour la modale
                if route_obj:
                    display_name = f"{route_obj['grade']} {route_obj['name']}"
                else:
                    display_name = "cette tentative"
                
                # Callback de confirmation
                def on_confirm():
                    delete_attempt(attempt["id"])
                    st.session_state.show_attempt_delete_success = True
                
                confirm_archive_dialog(display_name, on_confirm)
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
if st.session_state.show_attempt_add_success:
    st.toast("Tentative enregistrée !", icon="✅")
    st.session_state.show_attempt_add_success = False

if st.session_state.show_attempt_edit_success:
    st.toast("Tentative modifiée !", icon="✅")
    st.session_state.show_attempt_edit_success = False

if st.session_state.show_attempt_delete_success:
    st.toast("Tentative supprimée !", icon="✅")
    st.session_state.show_attempt_delete_success = False