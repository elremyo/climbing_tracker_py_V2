import streamlit as st
from utils.routes import get_routes, add_route
from utils.constants import ROUTE_COLORS, GRADES

st.title("🧗 Mes voies")

# Initialisation des flags session_state
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# --- Bouton pour afficher le formulaire ---
if st.button("➕ Ajouter une voie"):
    st.session_state.show_form = True

# --- Formulaire d'ajout ---
if st.session_state.show_form:
    with st.form("add_route_form"):
        name = st.text_input("Nom")

        # --- Selectbox pour les cotations ---
        grade = st.selectbox(
            "Cotation",
            options=GRADES
        )

        # --- Selectbox pour les couleurs + emojis ---
        color = st.selectbox(
            "Couleur",
            options=list(ROUTE_COLORS.keys()),
            format_func=lambda c: f"{ROUTE_COLORS[c]} {c}"
        )

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            errors = []

            if not name.strip():
                errors.append("Le nom de la voie est obligatoire.")
            if not grade:
                errors.append("La cotation est obligatoire.")
            if not color:
                errors.append("La couleur est obligatoire.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                # on stocke juste "Rouge", "Bleue"... pas l'emoji !
                add_route(name, grade, color)
                st.session_state.show_success = True
                st.session_state.show_form = False
                st.rerun()

# --- Liste des voies ---
routes = get_routes()
if routes:
    for route in routes:
        color_emoji = ROUTE_COLORS.get(route["color"], "❓")
        archived = route.get("archived", False)
        # Ligne d’affichage (emoji + couleur + cotation + nom)
        display = f"{color_emoji} **{route['grade']}** — {route['name']}"
        # Tag "archivée"
        if archived:
            display += " — 🔒 _Archivée_"
        st.markdown(display)

else:
    st.info("Aucune voie définie.")

# --- Affichage du message de succès ---
if st.session_state.show_success:
    st.toast("Voie ajoutée !",icon = "✅")
    st.session_state.show_success = False  # reset pour le prochain ajout
