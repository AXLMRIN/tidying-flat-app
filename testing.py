import pandas as pd
from pandas import Timestamp
print("Hello World")


deadlines = [Timestamp("2025-08-13"), Timestamp("2025-08-17")]

df = pd.DataFrame({
    "ID" : [1,2],
    "Task" : ["Salon", "SDB du bas"],
    "Status" : ["DONE", "TODO"],
    "Deadline": deadlines,
    "User" : ["Axel", "JM"]
})

df.to_csv("./data/calendar.csv", index = False)