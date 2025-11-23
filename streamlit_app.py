import streamlit as st

from pkg import (CONNECTION, render_history)

st.set_page_config(page_title = "Ménage",page_icon = "🧹")

st.write("# Tâches de la semaine")

with st.expander("How to use:", expanded = False):
    st.write((
    ":material/check: : Valider une tâche.\n\n"
    ":material/edit: : Éditer une tâches (statut `DONE, TODO, SKIPPED`) et l'utilisateur.ice. "
    "Les changements ne sont pas sauvegardés tant que vous n'avez pas appuyé sur "
    ":material/cloud_upload:\n\n"
    ":material/cloud_upload: : Sauvegarder les changements.\n\n"
    ":material/replay: : Force à recharger la page si vous ne voyez pas vos changements.\n\n"
    ))

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
st.write(f"Tâches de {user_filter if user_filter!='/' else 'tout le monde'}")
tasks_to_display, date_min, date_max = \
    CONNECTION.filter_calendar_per_user_and_date(user_filter)

i_element = 0

st.write(f"### Entre {date_min.strftime("%a %d")} et {date_max.strftime("%a %d")}")
cols = st.columns(3)
for iRow in range(len(tasks_to_display)):
    cols[iRow%3].write(render_history(tasks_to_display.iloc[iRow]), unsafe_allow_html=True)
    with cols[iRow%3].container(horizontal = True, horizontal_alignment = "center", vertical_alignment="center"):
        st.button(label = "", icon = ":material/check:", key = f"check-{i_element}", 
                            on_click=CONNECTION.check, 
                            args=[tasks_to_display.iloc[iRow]["ID"]])
        st.button(label = "", icon = ":material/edit:", key = f"edit-{i_element}", 
                            on_click=CONNECTION.dialog_edit_task, 
                            args=[tasks_to_display.iloc[iRow]["ID"]])
        st.button(label = "", icon = ":material/info:", key = f"info-{i_element}", 
                            on_click=CONNECTION.dialog_task_description, 
                            args=[tasks_to_display.iloc[iRow]["Task"]])
    i_element += 1
# ---
week_shift = st.select_slider(
    label = "Prochaines semaines",
    options = [1,2,3]
)

tasks_to_display_next, date_min_next, date_max_next = \
    CONNECTION.filter_calendar_per_user_and_date(user_filter, week_shift)

st.write(f"### Entre {date_min_next.strftime("%a %d")} et {date_max_next.strftime("%a %d")}")

cols_next = st.columns(3)
for iRow in range(len(tasks_to_display_next)):
    cols_next[iRow%3].write(render_history(tasks_to_display_next.iloc[iRow]), unsafe_allow_html=True)
    with cols_next[iRow%3].container(horizontal = True, horizontal_alignment = "center", vertical_alignment="center"):
        st.button(label = "", icon = ":material/check:", key = f"check-{i_element}", 
                            on_click=CONNECTION.check, 
                            args=[tasks_to_display_next.iloc[iRow]["ID"]])
        st.button(label = "", icon = ":material/edit:", key = f"edit-{i_element}", 
                            on_click=CONNECTION.dialog_edit_task, 
                            args=[tasks_to_display_next.iloc[iRow]["ID"]])
        st.button(label = "", icon = ":material/info:", key = f"info-{i_element}", 
                            on_click=CONNECTION.dialog_task_description, 
                            args=[tasks_to_display_next.iloc[iRow]["Task"]])
    i_element += 1
