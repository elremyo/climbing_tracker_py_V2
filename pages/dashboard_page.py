import streamlit as st
from data import get_routes, get_attempts
from services.stats_service import StatsService
from utils.formatting import format_date_fr

st.subheader("📊 Tableau de bord")

routes = get_routes()
attempts = get_attempts()

if not attempts:
    st.info("Aucune donnée pour le moment.")
    st.stop()

# Nombre total de tentatives
st.metric("📊 Nombre total de tentatives", len(attempts), border=True)

# Taux de réussite
success_rate = StatsService.calculate_success_rate(attempts)
st.metric("✅ Taux de réussite global", f"{success_rate:.1f} %", border=True)

# Dernière tentative
most_recent = max(attempts, key=lambda a: a["date"])
st.metric("📅 Dernière tentative", format_date_fr(most_recent["date"]), border=True)

# Voie la plus tentée
route, count = StatsService.get_most_attempted_route(attempts, routes)
if route:
    st.metric("💪 Voie la plus tentée", f"{route['name']} ({count} fois)", border=True)
else:
    st.metric("💪 Voie la plus tentée", f"Voie supprimée ({count} fois)", border=True)

# Voie la plus difficile réussie
attempt, route = StatsService.get_hardest_completed_route(attempts, routes)
if route:
    st.metric("🏆Meilleure difficulté", f"{route['grade']} ({route['name']})", border=True)

# Statistiques par niveau
st.subheader("Statistiques par niveau de difficulté")
grade_stats = StatsService.calculate_grade_stats(attempts, routes)

if grade_stats:
    for grade, (total, successful, rate) in grade_stats.items():
        st.markdown(f"**{grade}** : Réussi {successful} sur {total} -- {rate:.1f} %")
else:
    st.info("Aucune donnée par niveau de difficulté pour le moment.")