import pandas as pd
import streamlit as st

from pkg import CONNECTION, render_history, get_all_users
st.write("# History")

with st.container(horizontal = True):
    if st.button("", key = "force-reload", icon = ":material/replay:"):
        CONNECTION.force_reload()
    if st.button("", key = "upload_changes", icon = ":material/cloud_upload:"):
        CONNECTION.update_gsheet()
    if st.button("(DEGBUG) GENERATE"):
        CONNECTION.generate_new_tasks_to_calendar()

user = st.selectbox(
    label = "User", 
    options= ["/", *[user["name"] for user in get_all_users()]]
)
calendar = CONNECTION.get_all_history(user)
cols = st.columns(4)
for iRow in range(len(calendar)):
    cols[iRow%4].write(render_history(calendar.iloc[iRow]), unsafe_allow_html=True)
    cols[iRow%4].button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                        use_container_width = True, on_click=CONNECTION.dialog_edit_task, 
                        args=[calendar.iloc[iRow]["ID"]])