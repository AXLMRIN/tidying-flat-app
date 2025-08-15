import streamlit as st

def test():
    print("hello world")

st.write("# Gestion des tâches de nettoyage dans la colocation")
st.write("Liste des tâches à venir :")
cols = st.columns(3)
cols[0].write("JM")
cols[1].write("Salon")
cols[2].button("Done",on_click = test())