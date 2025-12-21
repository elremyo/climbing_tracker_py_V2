"""
Formulaires réutilisables pour routes et attempts.
"""
import streamlit as st
from datetime import date
from utils.constants import ROUTE_COLORS, GRADES

class RouteForm:
    """Formulaire de voie (add ou edit)"""
    
    @staticmethod
    def render(route=None, on_submit=None, on_cancel=None):
        """
        Affiche un formulaire de voie.
        
        Args:
            route: dict de la voie à éditer (None pour création)
            on_submit: callback(name, grade, color) appelé lors de la soumission
            on_cancel: callback() appelé lors de l'annulation
        """
        form_key = "edit_route_form" if route else "add_route_form"
        
        with st.form(form_key):
            name = st.text_input("Nom", value=route["name"] if route else "")
            
            grade = st.selectbox(
                "Cotation",
                options=GRADES,
                index=GRADES.index(route["grade"]) if route and route["grade"] in GRADES else 0
            )
            
            color = st.selectbox(
                "Couleur",
                options=list(ROUTE_COLORS.keys()),
                index=list(ROUTE_COLORS.keys()).index(route["color"]) if route and route["color"] in ROUTE_COLORS else None,
                format_func=lambda c: f"{ROUTE_COLORS[c]} {c}",
                placeholder="Sélectionne une couleur"
            )


            submitted = st.form_submit_button("Enregistrer", use_container_width=True,type="primary")
            cancel = st.form_submit_button("Annuler", use_container_width=True, type="secondary")
            
            if cancel and on_cancel:
                on_cancel()
            
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
                elif on_submit:
                    on_submit(name, grade, color)


class AttemptForm:
    """Formulaire de tentative (add ou edit)"""
    
    @staticmethod
    def render(routes, attempt=None, on_submit=None, on_cancel=None, fixed_route=None):
        """
        Affiche un formulaire de tentative.
        
        Args:
            routes: liste des voies disponibles
            attempt: dict de la tentative à éditer (None pour création)
            on_submit: callback(route_id, success, notes, attempt_date)
            on_cancel: callback() appelé lors de l'annulation
            fixed_route: dict de la voie fixe (non modifiable)
        """
        form_key = "edit_attempt_form" if attempt else "add_attempt_form"
        
        with st.form(form_key):
            # Sélecteur de voie OU affichage fixe
            if fixed_route:
                # Mode voie fixe : afficher les infos sans sélecteur
                color_emoji = ROUTE_COLORS.get(fixed_route["color"], "❓")
                st.markdown(f"**Voie :** {color_emoji} {fixed_route['grade']} - {fixed_route['name']}")
                route_id = fixed_route["id"]
            else:
                # Mode normal : sélecteur de voie
                route_mapping = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
                
                if attempt:
                    selected_route = next((k for k, v in route_mapping.items() if v == attempt['route_id']), "")
                    if not selected_route:
                        st.warning("⚠️ La voie associée à cette tentative a été supprimée.")
                        selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()))
                    else:
                        selected_route = st.selectbox(
                            "Voie",
                            [""] + list(route_mapping.keys()),
                            index=list(route_mapping.keys()).index(selected_route) + 1
                        )
                else:
                    selected_route = st.selectbox("Voie", [""] + list(route_mapping.keys()))
                
                route_id = route_mapping.get(selected_route, None)
            
            # Date
            if attempt:
                try:
                    from datetime import datetime
                    date_obj = datetime.fromisoformat(attempt["date"])
                    default_date = date_obj.date()
                except:
                    default_date = date.today()
            else:
                default_date = date.today()
            
            attempt_date = st.date_input("Date", value=default_date)
            
            # Succès et notes
            success = st.checkbox("Réussie", value=attempt.get("success", False) if attempt else False)
            notes = st.text_area("Notes", value=attempt.get("notes", "") if attempt else "")
            
            submitted = st.form_submit_button("Enregistrer", use_container_width=True, type="primary")
            cancel = st.form_submit_button("Annuler", use_container_width=True, type="secondary")
            
            if cancel and on_cancel:
                on_cancel()
            
            if submitted:
                errors = []
                if not fixed_route:  # Seulement vérifier si pas en mode voie fixe
                    if not selected_route or selected_route == "":
                        errors.append("Sélectionne une voie.")
                    elif route_id is None:
                        errors.append("Erreur : voie invalide sélectionnée.")
                if not attempt_date:
                    errors.append("Sélectionne une date.")
                
                if errors:
                    for err in errors:
                        st.error(err)
                elif on_submit:
                    on_submit(route_id, success, notes, attempt_date)