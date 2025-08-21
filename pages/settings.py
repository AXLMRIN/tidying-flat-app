import streamlit as st

from pkg import Task, get_all_tasks, User, get_all_users, render_user, render_task

st.set_page_config(page_title = "Flatify (free)",page_icon = "🧹")

st.write("# Settings")

######
cols_header_users = st.columns([0.8, 0.2])
cols_header_users[0].write("## Users")
cols_header_users[1].button(
    label = "Edit users",
    key = "users-edit",
    icon = ":material/edit:",
    use_container_width = True
)

######
cols_users = st.columns(3)
for i, user in enumerate(get_all_users()):
    cols_users[i%3].write(render_user(user), unsafe_allow_html=True)

######
st.write("---")
cols_header_tasks = st.columns([0.8, 0.2])
cols_header_tasks[0].write("## Tasks")
cols_header_tasks[1].button(
    label = "Edit tasks",
    key = "tasks-edit",
    icon = ":material/edit:",
    use_container_width = True
)

######
for i, task in enumerate(get_all_tasks()):
    st.write(render_task(task), unsafe_allow_html=True)
