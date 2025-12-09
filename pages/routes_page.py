import streamlit as st
from utils.routes import get_routes, add_route

st.title("🧗 Gestion des voies")

# Initialisation des flags session_state
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# --- Liste des voies ---
routes = get_routes()
if routes:
    st.subheader("Voies existantes")
    for route in routes:
        status = " [Archivée]" if route.get("archived") else ""
        st.write(f"{route['id']} — {route['name']} ({route['grade']}) — {route['color']}{status}")
else:
    st.info("Aucune voie définie.")

# --- Bouton pour afficher le formulaire ---
if st.button("➕ Ajouter une voie"):
    st.session_state.show_form = True

# --- Formulaire d'ajout ---
if st.session_state.show_form:
    with st.form("add_route_form"):
        name = st.text_input("Nom")
        grade = st.text_input("Cotation")
        color = st.text_input("Couleur")
        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            # --- Contrôles de saisie ---
            errors = []
            if not name.strip():
                errors.append("Le nom de la voie est obligatoire.")
            if not grade.strip():
                errors.append("La cotation est obligatoire.")
            if not color.strip():
                errors.append("La couleur est obligatoire.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                add_route(name, grade, color)
                st.session_state.show_success = True
                st.session_state.show_form = False
                st.rerun()  # recharge la page et affiche le succès via le flag

# --- Affichage du message de succès ---
if st.session_state.show_success:
    st.toast("Voie ajoutée !",icon = "✅")
    st.session_state.show_success = False  # reset pour le prochain ajout
