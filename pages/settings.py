import streamlit as st

from pkg import Task, get_all_tasks, User, get_all_users

st.write("# Settings")
cols = st.columns(2)
col_users = cols[0]
col_tasks = cols[1]


col_tasks.write("## Tasks")
for task in get_all_tasks():
    col_tasks.write(task.get_data())

col_users.write("## Users")
for user in get_all_users():
    col_users.write(user.get_data())