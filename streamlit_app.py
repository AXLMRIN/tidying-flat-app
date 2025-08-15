import streamlit as st

from pkg import test_function

st.write("# Gestion des tâches de nettoyage dans la colocation")
st.write("Liste des tâches à venir :")

st.button("TEST", on_click=test_function)