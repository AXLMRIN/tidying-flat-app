import pandas as pd
import streamlit as st

from . import status_index, get_all_users, CONNECTION

def dialog_edit_task(id : int, calendar : pd.DataFrame) -> None:
    st.write(f'ID : {id}')
    st.write("## Change Status")
    status = st.radio(
        label = "Status",
        options = ["TODO", "DONE", "SKIPPED"],
        horizontal = True,
        index = status_index(calendar.loc[calendar["ID"]==id,"Status"].item())
    )
    st.write("## Change user")
    st.write(f"Current user : {calendar.loc[calendar["ID"]==id,"User"].item()}")
    options = ["/", *[user["name"] for user in get_all_users()]]
    new_user = st.selectbox(
        label = "User", 
        options = options,
        index = options.index(calendar.loc[calendar["ID"]==id,"User"].item()),
    )
    if st.button("Submit"):
        # UPDATE the table
        calendar.loc[calendar["ID"]==id,"Status"] = status
        calendar.loc[calendar["ID"]==id,"User"] = new_user
        CONNECTION.update(worksheet="Calendar", data = calendar)
        st.rerun()