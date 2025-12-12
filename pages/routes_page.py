import streamlit as st
from utils.routes import get_routes, add_route, update_route, delete_route
from utils.constants import ROUTE_COLORS, GRADES
import pandas as pd

# Initialisation des flags session_state
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_add_success" not in st.session_state:
    st.session_state.show_add_success = False
if "show_edit_success" not in st.session_state:
    st.session_state.show_edit_success = False
if "show_delete_success" not in st.session_state:
    st.session_state.show_delete_success = False

# Initialisation des filtres
if "filter_colors" not in st.session_state:
    st.session_state.filter_colors = []
if "filter_grades" not in st.session_state:
    st.session_state.filter_grades = []
if "show_archived" not in st.session_state:
    st.session_state.show_archived = True


# --- FONCTION DE FILTRAGE ---
def filter_routes(routes):
    """Applique les filtres aux voies"""
    filtered = routes.copy()
    
    # Filtre par couleurs
    if st.session_state.filter_colors:
        filtered = [r for r in filtered if r["color"] in st.session_state.filter_colors]
    
    # Filtre par cotations
    if st.session_state.filter_grades:
        filtered = [r for r in filtered if r["grade"] in st.session_state.filter_grades]
    
    # Filtre archivées
    if not st.session_state.show_archived:
        filtered = [r for r in filtered if not r.get("archived", False)]
    
    return filtered


routes = get_routes()
filtered_routes = filter_routes(routes)

st.subheader(f"🧗 Mes voies ({len(filtered_routes)}/{len(routes)})")

# --- BOUTON AJOUTER (GROS POUR MOBILE) ---
if st.button("➕ Ajouter une voie", use_container_width=True):
    st.session_state.show_form = True

# --- FILTRES ---
with st.expander("🔍 Filtres"):
    # Filtre par couleurs
    selected_colors = st.multiselect(
        "Filtrer par couleurs",
        options=list(ROUTE_COLORS.keys()),
        default=st.session_state.filter_colors,
        format_func=lambda c: f"{ROUTE_COLORS[c]} {c}",
        placeholder="Toutes les couleurs"
    )
    st.session_state.filter_colors = selected_colors
    
    # Filtre par cotations
    selected_grades = st.multiselect(
        "Filtrer par cotations",
        options=GRADES,
        default=st.session_state.filter_grades,
        placeholder="Toutes les cotations"
    )
    st.session_state.filter_grades = selected_grades
    
    # Toggle archivées
    show_archived = st.checkbox(
        "Afficher les voies archivées",
        value=st.session_state.show_archived
    )
    if show_archived != st.session_state.show_archived:
        st.session_state.show_archived = show_archived
        st.rerun()
    
    # Bouton reset
    if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
        st.session_state.filter_colors = []
        st.session_state.filter_grades = []
        st.session_state.show_archived = True
        st.rerun()

st.divider()

# --- FORMULAIRE D'AJOUT ---
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

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Enregistrer", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
        
        if cancel:
            st.session_state.show_form = False
            st.rerun()
        
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
                add_route(name, grade, color)
                st.session_state.show_add_success = True
                st.session_state.show_form = False
                st.rerun()

@st.dialog("Éditer la voie")
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

# --- LISTE DES VOIES (RÉSULTATS FILTRÉS) ---
if filtered_routes:
    for route in filtered_routes:
        color_emoji = ROUTE_COLORS.get(route["color"], "❓")
        archived = route.get("archived", False)
        # Ligne d'affichage (emoji + couleur + cotation + nom)
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
    if routes:
        st.info("Aucune voie ne correspond aux filtres sélectionnés.")
    else:
        st.info("Aucune voie définie.")

# --- Affichage du message de succès ---
if st.session_state.show_add_success:
    st.toast("✅ Voie ajoutée !", icon="✅")
    st.session_state.show_add_success = False

if st.session_state.show_edit_success:
    st.toast("✅ Voie modifiée !", icon="✅")
    st.session_state.show_edit_success = False

if st.session_state.show_delete_success:
    st.toast("✅ Voie supprimée !", icon="✅")
    st.session_state.show_delete_success = False
