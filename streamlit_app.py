import pandas as pd
import streamlit as st

from pkg import (get_all_users, filter_calendar, 
    render_history, status_index, dialog_edit_task)

# Generate the calendar for the next month
# generate_calendar()
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
def dialog(id):
    dialog_edit_task(id, calendar)

cols = st.columns(4)
for iRow in range(len(tasks_to_display)):
    cols[iRow%4].write(render_history(tasks_to_display.iloc[iRow]), unsafe_allow_html=True)
    cols[iRow%4].button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                        use_container_width = True, on_click=dialog, 
                        args=[tasks_to_display.iloc[iRow]["ID"]])