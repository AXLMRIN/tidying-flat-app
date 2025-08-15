import pandas as pd
import numpy as np

from .TASK import Task, get_all_tasks

def test_function():
    print("## TEST ##")
    generate_calendar()

def generate_calendar():
    """generate calendar for the next month"""
    today = pd.Timestamp.now()
    calendar = pd.read_csv("./data/calendar.csv")
    # Sort the values so that the low index (ie 0) is the more recent
    calendar.sort_values("Deadline", ascending = False) 
    for task in get_all_tasks():
        task_name = task.get_data()["name"]
        print(task_name)
        sub_calendar = calendar.loc[calendar["Task"] == task_name, :]
        if len(sub_calendar) == 0: 
            # The task does not appear in the history
            last_occurence = today
        else:
            # Fetch the last iteration:
            last_occurence = sub_calendar.iloc[0]["Deadline"]
        print(f"{task["name"]} Last occurence : ", last_occurence)
