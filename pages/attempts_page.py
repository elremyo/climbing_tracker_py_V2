import streamlit as st
from utils.routes import get_routes
from utils.attempts import get_attempts, add_attempt, update_attempt, delete_attempt
from datetime import date, datetime, timedelta
from utils.constants import ROUTE_COLORS
from utils.formatting import format_date_fr

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


attempts = get_attempts()
routes = get_routes()

# Initialisation des flags session_state
if "show_attempt_form" not in st.session_state:
    st.session_state.show_attempt_form = False
if "show_attempt_success" not in st.session_state:
    st.session_state.show_attempt_success = False

# Initialisation des filtres dans session_state
if "filter_period" not in st.session_state:
    st.session_state.filter_period = "Tout"
if "filter_status" not in st.session_state:
    st.session_state.filter_status = "Toutes"
if "filter_routes" not in st.session_state:
    st.session_state.filter_routes = []
if "sort_order" not in st.session_state:
    st.session_state.sort_order = "Plus récent"


# --- FONCTION DE FILTRAGE ---
def filter_attempts(attempts, routes):
    """Applique les filtres aux tentatives"""
    filtered = attempts.copy()
    
    # Filtre par période
    if st.session_state.filter_period != "Tout":
        today = date.today()
        
        if st.session_state.filter_period == "Aujourd'hui":
            date_limit = today
            filtered = [a for a in filtered if datetime.fromisoformat(a["date"]).date() == date_limit]
        
        elif st.session_state.filter_period == "Cette semaine":
            # Lundi de cette semaine
            date_limit = today - timedelta(days=today.weekday())
            filtered = [a for a in filtered if datetime.fromisoformat(a["date"]).date() >= date_limit]
        
        elif st.session_state.filter_period == "Ce mois-ci":
            filtered = [a for a in filtered 
                       if datetime.fromisoformat(a["date"]).date().month == today.month 
                       and datetime.fromisoformat(a["date"]).date().year == today.year]
    
    # Filtre par statut
    if st.session_state.filter_status == "Réussies":
        filtered = [a for a in filtered if a.get("success")]
    elif st.session_state.filter_status == "Échouées":
        filtered = [a for a in filtered if not a.get("success")]
    
    # Filtre par voies
    if st.session_state.filter_routes:
        filtered = [a for a in filtered if a["route_id"] in st.session_state.filter_routes]
    
    # Tri
    if st.session_state.sort_order == "Plus récent":
        filtered = sorted(filtered, key=lambda a: a["date"], reverse=True)
    else:
        filtered = sorted(filtered, key=lambda a: a["date"], reverse=False)
    
    return filtered


# --- HEADER AVEC COMPTEUR ---
filtered_attempts = filter_attempts(attempts, routes)
st.subheader(f"🎯 Mes tentatives ({len(filtered_attempts)}/{len(attempts)})")

# --- BOUTON AJOUTER ---
if st.button("➕ Ajouter une tentative", key="add_attempt_button", use_container_width=True):
    st.session_state.show_attempt_form = True

# --- FILTRES RAPIDES (PILLS) ---
st.markdown("**Période**")

# Mapping entre les index et les valeurs
period_options = ["Semaine", "Mois", "Tout"]

# Trouver l'index actuel basé sur le session_state
if st.session_state.filter_period == "Cette semaine":
    current_index = 0
elif st.session_state.filter_period == "Ce mois-ci":
    current_index = 1
else:  # "Tout"
    current_index = 2

selected_period = st.pills(
    "filter_period_pills",
    options=period_options,
    selection_mode="single",
    default=period_options[current_index],
    label_visibility="collapsed"
)
# Convertir la sélection en valeur session_state
if selected_period == "Aujourd'hui":
    new_period = "Aujourd'hui"
elif selected_period == "Semaine":
    new_period = "Cette semaine"
elif selected_period == "Mois":
    new_period = "Ce mois-ci"
else:
    new_period = "Tout"
# Mettre à jour si changement
if new_period != st.session_state.filter_period:
    st.session_state.filter_period = new_period
    st.rerun()



st.markdown("**Statut**")
status_options = ["Toutes", "✅ Réussies", "❌ Échouées"]
# Trouver l'index actuel
if st.session_state.filter_status == "Toutes":
    status_index = 0
elif st.session_state.filter_status == "Réussies":
    status_index = 1
else:
    status_index = 2

selected_status = st.pills(
    "filter_status_pills",
    options=status_options,
    selection_mode="single",
    default=status_options[status_index],
    label_visibility="collapsed"
)

# Convertir en valeur session_state
if selected_status == "Toutes":
    new_status = "Toutes"
elif selected_status == "✅ Réussies":
    new_status = "Réussies"
else:
    new_status = "Échouées"

if new_status != st.session_state.filter_status:
    st.session_state.filter_status = new_status
    st.rerun()

# --- FILTRES AVANCÉS (COLLAPSIBLE) ---
with st.expander("🔍 Filtres avancés"):
    # Filtre par voies
    if routes:
        route_options = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
        selected_routes = st.multiselect(
            "Filtrer par voies",
            options=list(route_options.keys()),
            default=[k for k, v in route_options.items() if v in st.session_state.filter_routes],
            placeholder="Sélectionne une ou plusieurs voies"
        )
        st.session_state.filter_routes = [route_options[r] for r in selected_routes]
    
    # Tri
    sort_option = st.radio(
        "Trier par",
        ["Plus récent", "Plus ancien"],
        index=0 if st.session_state.sort_order == "Plus récent" else 1,
        horizontal=True
    )
    if sort_option != st.session_state.sort_order:
        st.session_state.sort_order = sort_option
        st.rerun()
    
    # Bouton reset
    if st.button("🔄 Réinitialiser les filtres", use_container_width=True):
        st.session_state.filter_period = "Tout"
        st.session_state.filter_status = "Toutes"
        st.session_state.filter_routes = []
        st.session_state.sort_order = "Plus récent"
        st.rerun()

st.divider()

# --- FORMULAIRE D'AJOUT ---
if st.session_state.show_attempt_form:
    if not routes:
        st.warning("Ajoute d'abord une voie avant d'enregistrer une tentative.")
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

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✅ Enregistrer", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
            
            if cancel:
                st.session_state.show_attempt_form = False
                st.rerun()
            
            if submitted:
                # --- Contrôles de saisie ---
                errors = []
                if not selected_route or selected_route == "":
                    errors.append("Sélectionne une voie.")
                elif route_id is None:
                    errors.append("Erreur : voie invalide sélectionnée.")
                
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
    st.toast("✅ Tentative enregistrée !", icon="✅")
    st.session_state.show_attempt_success = False


@st.dialog("Éditer la tentative")
def display_attempt_form_edit(attempt):
    with st.form("edit_attempt_form"):
        # Sélecteur de voie
        route_mapping = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
        selected_route = next((k for k, v in route_mapping.items() if v == attempt['route_id']), "")
        
        if not selected_route:
            st.warning("⚠️ La voie associée à cette tentative a été supprimée. Sélectionne une nouvelle voie.")
            selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()))
        else:
            selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()), 
                                        index=list(route_mapping.keys()).index(selected_route) + 1)
        
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
            if not selected_route or selected_route == "":
                errors.append("Sélectionne une voie.")
            elif route_id is None:
                errors.append("Erreur : voie invalide sélectionnée.")
            
            if not attempt_date:
                errors.append("Sélectionne une date.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                update_attempt(attempt.get("id"), route_id, success, notes, attempt_date)
                st.toast("✅ Tentative modifiée !", icon="✅")
                st.rerun()


# --- HISTORIQUE DES TENTATIVES (RÉSULTATS FILTRÉS) ---
if filtered_attempts:
    for a in filtered_attempts:
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
        date_str = format_date_fr(a["date"])

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
                st.toast("✅ Tentative supprimée !", icon="✅")
                st.rerun()
else:
    if attempts:
        st.info("Aucune tentative ne correspond aux filtres sélectionnés.")
    else:
        st.info("Aucune tentative enregistrée.")
