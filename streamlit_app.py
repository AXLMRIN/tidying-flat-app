import streamlit as st

from pkg import test_function

st.write("# Gestion des tâches de nettoyage dans la colocation")
st.write("Liste des tâches à venir :")
cols = st.columns(3)
cols[0].write("JM")
cols[1].write("Salon")
cols[2].button("Done",on_click = test_function())