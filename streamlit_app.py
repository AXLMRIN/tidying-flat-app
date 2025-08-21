import pandas as pd
import streamlit as st

from pkg import (CONNECTION, get_all_users, render_history)

st.set_page_config(page_title = "Flatify (free)",page_icon = "🧹")

st.write("# Tâches de la semaine")

with st.container(horizontal = True):
    if st.button("", key = "force-reload", icon = ":material/replay:"):
        CONNECTION.force_reload()
    if st.button("", key = "upload_changes", icon = ":material/cloud_upload:"):
        CONNECTION.update_gsheet()
    if st.button("(DEGBUG) GENERATE"):
        CONNECTION.generate_new_tasks_to_calendar()


user_filter = st.selectbox(
    label = "User", 
    options= ["/", *[user["name"] for user in get_all_users()]]
)
st.write("Liste des tâches à venir dans la semaine :")

# Filter the calendar to display
tasks_to_display = CONNECTION.filter_calendar_per_user_and_date(user_filter)

cols = st.columns(4)
for iRow in range(len(tasks_to_display)):
        st.button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                            on_click=CONNECTION.dialog_edit_task, 
                            args=[tasks_to_display.iloc[iRow]["ID"]])