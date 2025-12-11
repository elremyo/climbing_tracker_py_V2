import streamlit as st
from utils.routes import get_routes
from utils.attempts import get_attempts, add_attempt, edit_attempt, delete_attempt
from datetime import date, datetime
from utils.constants import ROUTE_COLORS

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


st.title("🎯 Mes tentatives")

# Initialisation des flags session_state
if "show_attempt_form" not in st.session_state:
    st.session_state.show_attempt_form = False
if "show_attempt_success" not in st.session_state:
    st.session_state.show_attempt_success = False

routes = get_routes()

# --- Bouton pour afficher le formulaire ---
if st.button("➕ Ajouter une tentative", key="add_attempt_button"):
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



@st.dialog("Éditer la tentative ")
def display_attempt_form_edit(attempt):
    with st.form("edit_attempt_form"):
        # Sélecteur de voie
        route_mapping = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
        selected_route = next((k for k, v in route_mapping.items() if v == attempt['route_id']), "")
        selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()), index=list(route_mapping.keys()).index(selected_route) + 1)
        route_id = route_mapping.get(selected_route, None)

        # Date picker
        try:
            date_obj = datetime.fromisoformat(attempt["date"])
            default_date = date_obj.date()
        except:
            default_date = date.today()
        attempt_date = st.date_input("Date", value=default_date)

        success = st.checkbox("Réussie", value=attempt.get("success", False))
        notes = st.text_area("Notes", value=attempt.get("notes", ""))

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            # --- Contrôles de saisie ---
            errors = []
            if not selected_route or selected_route == "" or not attempt_date:
                errors.append("Sélectionne une voie.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                edit_attempt(attempt.get("id"), route_id, success, notes, attempt_date)
                st.success("Tentative modifiée !")
                st.rerun()



# --- Historique des tentatives ---
attempts = get_attempts()
if attempts:
    for a in attempts:

        # --- Récup infos de la voie ---
        route = next((r for r in routes if r['id'] == a['route_id']), None)
        if route:
            route_name = route["name"]
            route_color = ROUTE_COLORS.get(route["color"], "❓")
            route_grade = route["grade"]
        else:
            route_name = "Voie supprimée"
            route_color = "❓"
            route_grade = ""

        # --- Format date JJ/MM/AA ---
        try:
            date_obj = datetime.fromisoformat(a["date"])
            date_str = date_obj.strftime("%d/%m/%y")
        except:
            date_str = a["date"]  # fallback si format inattendu

        # --- Status ---
        status = "✅ Réussie" if a.get("success") else "❌ Échouée"

        # --- Notes : si vide → on n'affiche rien du tout ---
        notes = a.get("notes")
        if notes and notes.strip():
            notes_display = f" — *{notes}*"
        else:
            notes_display = ""

        col_data, col_edit, col_del = st.columns([8, 1, 1])
        with col_data:
            # --- affichage ---
            st.markdown(
                f"{date_str} — {route_color} **{route_grade} {route_name}** — {status}{notes_display}"
            )
        with col_edit:
            btn_key = f"attempt_{a.get('id')}"
            if st.button("", key=btn_key+"_edit", icon="✏️"):
                display_attempt_form_edit(a)
        with col_del:
            if st.button("", key=btn_key+"_del", icon="🗑️"):
                delete_attempt(a.get("id"))
                st.success("Tentative supprimée.")
                st.rerun()
else:
    st.info("Aucune tentative enregistrée.")
