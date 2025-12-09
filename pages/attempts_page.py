import streamlit as st
from utils.routes import get_routes
from utils.attempts import get_attempts, add_attempt

st.title("🎯 Tentatives")
routes = get_routes()
if not routes:
    st.info("Ajoute d’abord une voie.")
else:
    mapping = {f"{r['name']} ({r['grade']})": r["id"] for r in routes}
    sel = st.selectbox("Voie", list(mapping.keys()))
    route_id = mapping[sel]
    success = st.checkbox("Réussie")
    notes = st.text_area("Notes")
    if st.button("Ajouter tentative"):
        add_attempt(route_id, success, notes)
        st.success("Tentative enregistrée.")
        st.experimental_rerun()
st.subheader("Historique des tentatives")
st.write(get_attempts())
