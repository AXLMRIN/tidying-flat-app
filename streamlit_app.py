import pandas as pd
import streamlit as st

from pkg import (test_function, generate_calendar, get_all_users, filter_calendar, 
    render_history, status_index)

# Generate the calendar for the next month
generate_calendar()
calendar = pd.read_csv("./data/calendar.csv")

st.write("# Gestion des tâches de nettoyage dans la colocation")
user_filter = st.selectbox(
    label = "User", 
    options= ["/", *[user["name"] for user in get_all_users()]]
)
st.write("Liste des tâches à venir dans la semaine :")

# Filter the calendar to display
tasks_to_display = filter_calendar(calendar, user_filter)
tasks_to_display = tasks_to_display.sort_values("Deadline",ascending=False)

@st.dialog("Cast your vote")
def test(id):
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
        calendar.to_csv("./data/calendar.csv")
        st.rerun()

cols = st.columns(4)
for iRow in range(len(tasks_to_display)):
    cols[iRow%4].write(render_history(tasks_to_display.iloc[iRow]), unsafe_allow_html=True)
    cols[iRow%4].button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                        use_container_width = True, on_click=test, 
                        args=[tasks_to_display.iloc[iRow]["ID"]])