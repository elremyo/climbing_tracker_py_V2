import streamlit as st
from utils.routes import get_routes, add_route, update_route, delete_route
from utils.constants import ROUTE_COLORS, GRADES

routes = get_routes()

st.subheader(f"🧗 Mes voies ({len(routes)})")

# Initialisation des flags session_state
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_add_success" not in st.session_state:
    st.session_state.show_add_success = False
if "show_edit_success" not in st.session_state:
    st.session_state.show_edit_success = False
if "show_delete_success" not in st.session_state:
    st.session_state.show_delete_success = False

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
                st.session_state.show_add_success = True
                st.session_state.show_form = False
                st.rerun()

@st.dialog("Éditer la route ")
def display_route_form_edit(route):
    with st.form("edit_route_form"):
        name = st.text_input("Nom", value=route["name"])

        # --- Selectbox pour les cotations ---
        grade = st.selectbox(
            "Cotation",
            options=GRADES,
            index=GRADES.index(route["grade"]) if route["grade"] in GRADES else 0
        )

        # --- Selectbox pour les couleurs + emojis ---
        color = st.selectbox(
            "Couleur",
            options=list(ROUTE_COLORS.keys()),
            index=list(ROUTE_COLORS.keys()).index(route["color"]) if route["color"] in ROUTE_COLORS else 0,
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
                update_route(route["id"], name=name, grade=grade, color=color)
                st.session_state.show_edit_success = True
                st.rerun()

# --- Liste des voies ---
if routes:
    for route in routes:
        color_emoji = ROUTE_COLORS.get(route["color"], "❓")
        archived = route.get("archived", False)
        # Ligne d’affichage (emoji + couleur + cotation + nom)
        display = f"{color_emoji} **{route['grade']}** — {route['name']}"
        # Tag "archivée"
        if archived:
            display += " — 🔒 _Archivée_"
        col_data, col_edit, col_del = st.columns([8, 1, 1])
        with col_data:
            st.markdown(display)
        with col_edit:
            btn_key = f"route_{route.get('id')}"
            if st.button("", key=btn_key+"_edit", icon="✏️"):
                # Afficher le formulaire d'édition
                display_route_form_edit(route)
        with col_del:
            if st.button("", key=btn_key+"_del", icon="🗑️"):
                delete_route(route.get("id"))
                st.session_state.show_delete_success = True
                st.rerun()

else:
    st.info("Aucune voie définie.")

# --- Affichage du message de succès ---
if st.session_state.show_add_success:
    st.toast("Voie ajoutée !",icon = "✅")
    st.session_state.show_add_success = False  # reset pour le prochain ajout

if st.session_state.show_edit_success:
    st.toast("Voie modifiée !", icon="✅")
    st.session_state.show_edit_success = False  # reset pour la prochaine édition

if st.session_state.show_delete_success:
    st.toast("Voie supprimée !", icon="✅")
    st.session_state.show_delete_success = False  # reset pour la prochaine suppression
