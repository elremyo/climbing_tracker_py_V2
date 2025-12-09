import streamlit as st
from utils.routes import get_routes
from utils.attempts import get_attempts, add_attempt
from datetime import date

st.title("🎯 Gestion des tentatives")

# Initialisation des flags session_state
if "show_attempt_form" not in st.session_state:
    st.session_state.show_attempt_form = False
if "show_attempt_success" not in st.session_state:
    st.session_state.show_attempt_success = False

routes = get_routes()

# --- Historique des tentatives ---
st.subheader("Historique des tentatives")
attempts = get_attempts()
if attempts:
    for a in attempts:
        route_name = next((r['name'] for r in routes if r['id'] == a['route_id']), "Voie supprimée")
        status = "✅ Réussie" if a.get("success") else "❌ Échouée"
        st.write(f"{a['date']} — {route_name} — {status} — {a.get('notes','')}")
else:
    st.info("Aucune tentative enregistrée.")

# --- Bouton pour afficher le formulaire ---
if st.button("➕ Ajouter une tentative"):
    st.session_state.show_attempt_form = True

# --- Formulaire d'ajout ---
if st.session_state.show_attempt_form:
    if not routes:
        st.warning("Ajoute d’abord une voie avant d’enregistrer une tentative.")
    else:
        with st.form("add_attempt_form"):
            # Sélecteur de voie vide par défaut
            route_mapping = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
            selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()))
            route_id = route_mapping.get(selected_route, None)

            # Date picker par défaut aujourd'hui
            attempt_date = st.date_input("Date", value=date.today())

            success = st.checkbox("Réussie")
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Enregistrer")
            if submitted:
                # --- Contrôles de saisie ---
                errors = []
                if not selected_route or selected_route == "":
                    errors.append("Sélectionne une voie.")
                if not attempt_date:
                    errors.append("Sélectionne une date.")

                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    add_attempt(route_id, success, notes, attempt_date)
                    st.session_state.show_attempt_success = True
                    st.session_state.show_attempt_form = False
                    st.rerun()

# --- Message de succès ---
if st.session_state.show_attempt_success:
    st.success("Tentative enregistrée !")
    st.session_state.show_attempt_success = False
