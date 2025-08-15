import os 

import numpy as np
import pandas as pd

def name_to_filename(name : str) -> str:
    filename = ''.join(c for c in name if c.isascii())
    return filename + ".txt"

def del_task(filename : str):
    list_of_existing_tasks = os.listdir('./data/tasks')
    if filename in list_of_existing_tasks:
        try:
            os.remove(f"./data/tasks/{filename}")
            print(f"File {filename} was successfully deleted")
        except Exception as e:
            print((f"ERROR: file {filename} exists in ./data/tasks but could not "
                   f"be deleted because:\n{e}"))

    else:
        print(f"ERROR: file {filename} does not exist in ./data/tasks")

def del_user(filename : str):
    list_of_existing_tasks = os.listdir('./data/users')
    if filename in list_of_existing_tasks:
        try:
            os.remove(f"./data/users/{filename}")
            print(f"File {filename} was successfully deleted")
        except Exception as e:
            print((f"ERROR: file {filename} exists in ./data/users but could not "
                   f"be deleted because:\n{e}"))

    else:
        print(f"ERROR: file {filename} does not exist in ./data/users")

def filter_calendar(calendar : pd.DataFrame, user : str = "/") -> pd.DataFrame:
    # Transform the "Deadline" column (str) to Timestamp to be able to use the <
    # operator
    calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)

    # Fetch the IDs for the rows corresponding to tasks which due date are nigh
    date_max = pd.Timestamp.now() + pd.Timedelta(weeks = 1)
    date_min = pd.Timestamp.now() - pd.Timedelta(days = 1)

    selected_rows_date = calendar.loc[
        (calendar["Deadline"] >= date_min) & (calendar["Deadline"] <= date_max),
        "ID"
    ]

    # Fetch the IDs for the rows corresponding to tasks associated to a specific
    # user, if provided
    if user != "/":
        selected_rows_user = calendar.loc[
            calendar["User"] == user,
            "ID"
        ]   
    else:
        # Take them all because of the way we combine the lists, see below
        selected_rows_user = calendar["ID"]
    
    # Fetch the IDs that have not been completed
    selected_rows_late = calendar.loc[
        (calendar["Status"] != "DONE")&(calendar["Status"] != "SKIPPED")&\
            (calendar["Deadline"] < date_min),
        "ID"
    ]

    # Combine IDs from the user and date
    selected_IDs = [ID for ID in selected_rows_date if ID in selected_rows_user]
    # Add the IDs for the late tasks, technically, the selected_rows_date and the
    # selected_rows_late are mutually exclusive
    selected_IDs += selected_rows_late.to_list()

    return calendar.loc[np.isin(calendar["ID"], selected_IDs), :]

def status_index(status) -> int:
    # Make it cleaner
    if status == "TODO": return 0
    elif status == "DONE" : return 1
    elif status == "SKIPPED" : return 2
    else:return None