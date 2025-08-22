import streamlit as st

from pkg import (CONNECTION, render_history)

st.set_page_config(page_title = "Flatify (free)",page_icon = "🧹")

st.write("# Tâches de la semaine")

if st.button("(DEGBUG) GENERATE"):
    CONNECTION.generate_new_tasks_to_calendar()

with st.container(horizontal = True, vertical_alignment = "bottom"):
    user_filter = st.selectbox(
        label = "User", 
        options= CONNECTION.user_names
    )
    if st.button("", key = "force-reload", icon = ":material/replay:"):
        CONNECTION.force_reload()
    if st.button("", key = "upload_changes", icon = ":material/cloud_upload:"):
        CONNECTION.update_gsheet()

# Filter the calendar to display
tasks_to_display = CONNECTION.filter_calendar_per_user_and_date(user_filter)

cols = st.columns(3)
for iRow in range(len(tasks_to_display)):
    cols[iRow%3].write(render_history(tasks_to_display.iloc[iRow]), unsafe_allow_html=True)
    with cols[iRow%3].container(horizontal = True, horizontal_alignment = "center", vertical_alignment="center"):
        st.button(label = "", icon = ":material/check:", key = f"check-{iRow}", 
                            on_click=CONNECTION.check, 
                            args=[tasks_to_display.iloc[iRow]["ID"]])
        st.button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                            on_click=CONNECTION.dialog_edit_task, 
                            args=[tasks_to_display.iloc[iRow]["ID"]])