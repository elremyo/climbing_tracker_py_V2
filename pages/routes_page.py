import streamlit as st
from data import get_routes, add_route, update_route
from services.session_state_service import SessionStateService
from services.filter_service import FilterService
from components.filters import FilterComponents
from components.cards import RouteCard
from components.dialogs import add_route_dialog,edit_route_dialog
from services.auth_service import AuthService

# Protection : rediriger vers login si non connecté
AuthService.require_auth()

st.set_page_config(
    page_title="Voies"
)

# Initialisation
SessionStateService.init_routes_state()

# Chargement des données
routes = get_routes()
filtered_routes = FilterService.filter_routes(routes)

# Header
st.subheader(f"Mes voies ({len(filtered_routes)}/{len(routes)})")

# Boutton d'ajout
if st.button("Ajouter une voie", icon=":material/add:", use_container_width=True, type="primary"):
    def save_handler(name, grade, color):
        add_route(name, grade, color)
        st.session_state.show_add_success = True    
    add_route_dialog(save_handler)


# Filtres
with st.expander("Filtres"):
    FilterComponents.colors_multiselect()
    FilterComponents.grades_range_slider()
    
    if st.button("Réinitialiser les filtres",icon=":material/replay:", use_container_width=True):
        SessionStateService.reset_routes_filters()
        st.rerun()

st.divider()

# Liste des voies
if filtered_routes:
    for route in filtered_routes:
        def make_click_handler(r):
            def handler():
                st.query_params.from_dict({"route_id": str(r["id"])})
                st.switch_page("pages/route_detail_page.py", query_params={"route_id": str(r["id"])})
            return handler

        def make_edit_handler(r):
            def handler():
                def save_handler(name, grade, color):
                    update_route(r["id"], name=name, grade=grade, color=color)
                    st.session_state.show_edit_success = True
                edit_route_dialog(r, save_handler)
            return handler

        RouteCard.render(
            route,
            on_click=make_click_handler(route),
            on_edit=make_edit_handler(route)
        )
else:
    if routes:
        st.info("Aucune voie ne correspond aux filtres sélectionnés.")
    else:
        st.info("Aucune voie définie.")

# Messages de succès
if st.session_state.show_add_success:
    st.toast("Voie ajoutée !", icon="✅")
    st.session_state.show_add_success = False

if st.session_state.show_edit_success:
    st.toast("Voie modifiée !", icon="✅")
    st.session_state.show_edit_success = False