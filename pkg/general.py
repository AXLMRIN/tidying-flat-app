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

def status_index(status) -> int:
    # Make it cleaner
    if status == "TODO": return 0
    elif status == "DONE" : return 1
    elif status == "SKIPPED" : return 2
    else:return None