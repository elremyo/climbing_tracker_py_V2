import streamlit as st
from utils.routes import get_routes, add_route

st.title("🧗 Voies")
routes = get_routes()
if routes:
    st.subheader("Voies existantes")
    for r in routes:
        st.write(f"{r['id']} — {r['name']} ({r['grade']}) — {r['color']}")
else:
    st.info("Aucune voie définie.")
st.subheader("Ajouter une voie")
name = st.text_input("Nom")
grade = st.text_input("Cotation")
color = st.text_input("Couleur")
if st.button("Ajouter voie"):
    add_route(name, grade, color)
    st.success("Voie ajoutée !")
    st.experimental_rerun()  # ou st.rerun() selon version