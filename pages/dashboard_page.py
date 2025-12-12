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
else:
    # ✅ Gestion du cas où la voie a été supprimée
    st.metric("💪 Voie la plus tentée", f"Voie supprimée ({most_common_count} fois)", border=True)

# Voie la plus difficile réussie
# ✅ On filtre pour ne garder que les tentatives avec des voies existantes
successful_attempts_with_routes = []
for a in attempts:
    if a["success"]:
        route = next((r for r in routes if r["id"] == a["route_id"]), None)
        if route:  # On ne garde que si la voie existe toujours
            successful_attempts_with_routes.append((a, route))

if successful_attempts_with_routes:
    # Tri par difficulté (index dans GRADES)
    successful_attempts_sorted = sorted(
        successful_attempts_with_routes,
        key=lambda item: GRADES.index(item[1]["grade"]) if item[1]["grade"] in GRADES else -1,
        reverse=True
    )
    hardest_attempt, hardest_route = successful_attempts_sorted[0]
    st.metric("🏆Meilleure difficulté", f"{hardest_route['grade']} ({hardest_route['name']})", border=True)

# Affichage des statistiques par niveau de difficulté
st.subheader("Statistiques par niveau de difficulté")
grade_stats = {}
for grade in GRADES:
    # ✅ On filtre pour ne compter que les tentatives avec voies existantes
    grade_attempts = []
    for a in attempts:
        route = next((r for r in routes if r["id"] == a["route_id"]), None)
        if route and route.get("grade") == grade:
            grade_attempts.append(a)
    
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
