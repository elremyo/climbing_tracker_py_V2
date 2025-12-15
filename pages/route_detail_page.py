import streamlit as st
from data import get_routes, get_attempts
from services.route_stats_service import RouteStatsService
from components.cards import AttemptCard
from utils.constants import ROUTE_COLORS, ROUTE_TYPES
from utils.formatting import format_date_fr

st.write("# Détail de la voie")

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

# Récupérer toutes les tentatives de cette voie
attempts = get_attempts()
route_attempts = [a for a in attempts if str(a["route_id"]) == str(route_id)]

# Calculer les stats
stats = RouteStatsService.get_route_stats(route_attempts)

# ===== HEADER =====
col1, col2 = st.columns([1, 6])
with col1:
    if st.button("", icon=":material/arrow_back:", help="Retour", type="tertiary"):
        st.switch_page("pages/routes_page.py")

with col2:
    color_emoji = ROUTE_COLORS.get(route["color"], "❓")
    route_type = route.get("type")
    type_display = f" • {ROUTE_TYPES.get(route_type, route_type)}" if route_type else ""
    archived_badge = " :red-badge[Archivée]" if route.get("archived") else ""
    st.subheader(f"{color_emoji} {route['grade']} - {route['name']}{type_display}{archived_badge}")

# ===== STATISTIQUES PRINCIPALES =====


if route_attempts:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tentatives", stats['total'], border=True)

    with col2:
        if stats['total'] > 0:
            st.metric(
                "Taux de réussite",
                f"{stats['success_rate']:.0f}%",
                border=True
            )
        else:
            st.metric("Taux de réussite", "—", border=True)

    with col3:
        if stats['first_attempt_date']:
            st.metric(
                "Première tentative",
                format_date_fr(stats['first_attempt_date']),
                border=True
            )
        else:
            st.metric("Première tentative", "—", border=True)

    with col4:
        if stats['last_attempt_date']:
            st.metric(
                "Dernière tentative",
                format_date_fr(stats['last_attempt_date']),
                border=True
            )
        else:
            st.metric("Dernière tentative", "—", border=True)
    


# ===== HISTORIQUE DES TENTATIVES =====
st.divider()

st.markdown("### 🎯 Historique des tentatives")

if route_attempts:
    # Trier par date (plus récentes en haut)
    sorted_attempts = RouteStatsService.get_progression_timeline(route_attempts)
    
    for attempt in sorted_attempts:
        def make_edit_handler(a):
            def handler():
                from components.dialogs import edit_attempt_dialog
                def save_handler(route_id, success, notes, attempt_date):
                    from data import update_attempt
                    update_attempt(a["id"], route_id, success, notes, attempt_date)
                    st.toast("✅ Tentative modifiée !", icon="✅")
                edit_attempt_dialog(a, [route], save_handler)
            return handler

        def make_delete_handler(a):
            def handler():
                from components.dialogs import confirm_archive_dialog
                from data import delete_attempt
                def on_confirm():
                    delete_attempt(a["id"])
                    st.toast("✅ Tentative supprimée !", icon="✅")
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

if st.button("Ajouter une tentative", icon=":material/add:", type="primary"):
    st.switch_page("pages/attempts_page.py")