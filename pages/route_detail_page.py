import streamlit as st
from data import get_routes, get_attempts, add_attempt, update_attempt, delete_attempt
from components.dialogs import add_attempt_dialog, edit_attempt_dialog, confirm_archive_dialog
from services.route_stats_service import RouteStatsService
from components.cards import AttemptCard
from utils.constants import ROUTE_COLORS
from utils.formatting import format_date_fr
from services.auth_service import AuthService

# Protection : rediriger vers login si non connecté
AuthService.require_auth()



# Récupération du route_id depuis les query params
query_params = st.query_params
route_id = st.query_params.get("route_id", None) 

# Si pas de route_id, rediriger vers la page des voies
if not route_id:
    st.warning("Aucune voie sélectionnée")
    if st.button("← Retour aux voies"):
        st.switch_page("pages/routes_page.py")
    st.stop()

# Chargement des données
routes = get_routes()
route = next((r for r in routes if str(r["id"]) == str(route_id)), None)

# Si la voie n'existe pas
if not route:
    st.error("Voie introuvable")
    if st.button("← Retour aux voies"):
        st.switch_page("pages/routes_page.py")
    st.stop()

st.set_page_config(
    page_title=f"Détail : {route['name']}"
)

# Récupérer toutes les tentatives de cette voie
attempts = get_attempts()
route_attempts = [a for a in attempts if str(a["route_id"]) == str(route_id)]

# Calculer les stats
stats = RouteStatsService.get_route_stats(route_attempts)

# ===== HEADER =====
st.subheader(" Détail de la voie")

with st.container(border=False, vertical_alignment="bottom", horizontal=True, gap="small"):
    if st.button("", icon=":material/arrow_back:", help="Retour", type="tertiary"):
            st.switch_page("pages/routes_page.py")

    color_emoji = ROUTE_COLORS.get(route["color"], "❓")
    archived_badge = " :red-badge[Archivée]" if route.get("archived") else ""
    st.subheader(f"{color_emoji} {route['grade']} - {route['name']}{archived_badge}")


# ===== STATISTIQUES PRINCIPALES =====


if route_attempts:
    if stats['total'] > 0:
        st.space(size="small")
        st.markdown(f"##### {stats['total']} tentatives ({stats['success_rate']:.0f}% de réussite)")


# ===== HISTORIQUE DES TENTATIVES =====
st.divider()
st.markdown("### Historique des tentatives")

#Bouton d'ajout
if st.button("Ajouter une tentative", icon=":material/add:", type="primary"):
    def save_handler(route_id, success, notes, attempt_date):
        add_attempt(route_id, success, notes, attempt_date)
        st.session_state.show_attempt_add_success = True
    
    add_attempt_dialog([route], save_handler, fixed_route=route)

#Liste des tentatives
if route_attempts:
    # Trier par date (plus récentes en haut)
    sorted_attempts = RouteStatsService.get_progression_timeline(route_attempts)
    
    for attempt in sorted_attempts:
        def make_edit_handler(a):
            def handler():
                def save_handler(route_id, success, notes, attempt_date):
                    update_attempt(a["id"], route_id, success, notes, attempt_date)
                    st.session_state.show_attempt_edit_success = True
                edit_attempt_dialog(a, [route], save_handler)
            return handler

        def make_delete_handler(a):
            def handler():
                def on_confirm():
                    delete_attempt(a["id"])
                    st.session_state.show_attempt_delete_success = True
                confirm_archive_dialog(f"tentative du {format_date_fr(a['date'])}", on_confirm)
            return handler

        AttemptCard.render(
            attempt,
            route,
            show_route_info=False,
            on_edit=make_edit_handler(attempt),
            on_delete=make_delete_handler(attempt)
        )

else:
    st.info("Aucune tentative enregistrée pour cette voie.")

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