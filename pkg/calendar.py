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
    calendar = calendar.sort_values("Deadline", ascending = False) 
    for task in get_all_tasks():
        task_name = task["name"]
        sub_calendar = calendar.loc[calendar["Task"] == task_name, :]
        if len(sub_calendar) == 0: 
            # The task does not appear in the history
            last_occurence = today
        else:
            # Fetch the last iteration:
            last_occurence = pd.Timestamp(sub_calendar.iloc[0]["Deadline"])
        # Reset the time
        last_occurence = last_occurence.replace(hour = 0, minute = 0, second = 0, 
            microsecond = 0)
        # Add events for the next month
        next_occurence = last_occurence + pd.Timedelta(weeks = task["frequency"])
        while next_occurence < today + pd.Timedelta(weeks = 4):
            calendar = pd.concat(
                [
                    calendar,
                    pd.DataFrame({
                        "ID" : len(calendar),
                        "Task" : task_name,
                        "Status" : "TODO",
                        "Deadline" : next_occurence,
                        "User" : np.nan
                    }),
                ], 
                ignore_index=True
            )
            next_occurence = next_occurence + pd.Timedelta(weeks = task["frequency"])
    calendar.to_csv("./data/calendar.csv", index = False)

