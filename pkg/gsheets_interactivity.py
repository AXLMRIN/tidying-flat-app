import pandas as pd

from . import CONNECTION

def update_sheet(data : pd.DataFrame, worksheet : str):
    CONNECTION.update(worksheet = worksheet, data = data)

def initialise_calendar():
    df = pd.read_csv("./data/calendar.csv")
    df = df.drop(["Unnamed: 0.4","Unnamed: 0.3","Unnamed: 0.2","Unnamed: 0.1","Unnamed: 0"], axis = 1)
    CONNECTION.create(worksheet = "Calendar", data = df)
    return "DONE"