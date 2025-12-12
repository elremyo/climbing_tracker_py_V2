import streamlit as st
from utils.routes import get_routes
from utils.attempts import get_attempts
from utils.constants import ROUTE_COLORS, GRADES
from utils.formatting import format_date_fr

st.subheader("📊 Tableau de bord")

routes = get_routes()
attempts = get_attempts()

if not attempts:
    st.info("Aucune donnée pour le moment.")
    st.stop()

# Nombre total de tentatives
total_attempts = len(attempts)
st.metric("📊 Nombre total de tentatives", total_attempts, border=True)

# Taux de réussite global
successful_attempts = sum(1 for a in attempts if a["success"])
success_rate = (successful_attempts / total_attempts) * 100
st.metric("✅ Taux de réussite global", f"{success_rate:.1f} %", border=True)

# Tentative la plus récente
most_recent_attempt = max(attempts, key=lambda a: a["date"])
attempt_date_str = format_date_fr(most_recent_attempt["date"])
st.metric("📅 Dernière tentative", attempt_date_str, border=True)

# Voie la plus tentée
from collections import Counter
route_counter = Counter(a["route_id"] for a in attempts)
most_common_route_id, most_common_count = route_counter.most_common(1)[0]
most_common_route = next((r for r in routes if r["id"] == most_common_route_id), None)
if most_common_route:
    route_name = most_common_route["name"]
    st.metric("💪 Voie la plus tentée", f"{route_name} ({most_common_count} fois)", border=True)

# Voie la plus difficile réussie
successful_attempts_sorted = sorted(
    (a for a in attempts if a["success"]),
    key=lambda a: GRADES.index(next((r for r in routes if r["id"] == a["route_id"]), {}).get("grade", GRADES[0])),
    reverse=True
)
if successful_attempts_sorted:
    hardest_attempt = successful_attempts_sorted[0]
    hardest_route = next((r for r in routes if r["id"] == hardest_attempt["route_id"]), None)
    if hardest_route:
        date_str = format_date_fr(hardest_attempt["date"])
        st.metric("🏆Meilleure difficulté", f"{hardest_route['grade']} ({hardest_route['name']})", border=True)

# Affichage des statistiques par niveau de difficulté
st.subheader("Statistiques par niveau de difficulté")
grade_stats = {}
for grade in GRADES:
    grade_attempts = [a for a in attempts if next((r for r in routes if r["id"] == a["route_id"]), {}).get("grade") == grade]
    if grade_attempts:
        total = len(grade_attempts)
        successful = sum(1 for a in grade_attempts if a["success"])
        rate = (successful / total) * 100
        grade_stats[grade] = (total, successful, rate)
if grade_stats:
    for grade, (total, successful, rate) in grade_stats.items():
        st.markdown(f"**{grade}** : Réussi {successful} sur {total} -- {rate:.1f} %")
else:
    st.info("Aucune donnée par niveau de difficulté pour le moment.")
