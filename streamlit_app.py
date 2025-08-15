import streamlit as st

from pkg import test_function, get_list_of_tasks

st.write("# Gestion des tâches de nettoyage dans la colocation")
st.write("Liste des tâches à venir :")

list_of_tasks = get_list_of_tasks()
for task in list_of_tasks:
    st.write(task)

cols = st.columns(3)
cols[0].write("JM")
cols[1].write("Salon")
cols[2].button("Done",on_click = test_function())