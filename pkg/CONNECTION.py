import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class Connection:
    def __init__(self, worksheet : str) -> None:
        # initialise variables
        self.worksheet = worksheet
        self.__connection = st.connection("gsheets", type = GSheetsConnection)
        try:
            # read the data
            self.data : pd.DataFrame|None= self.__connection.read(worksheet = worksheet)
        except:
            print(("WARNING: force reload - Could not read the worksheet "
                   f"({self.worksheet})."))
            self.data : pd.DataFrame|None = None

    def force_reload(self) -> None:
        try:
            self.data = self.__connection.read(worksheet = self.worksheet, ttl = 1)
        except:
            print(("WARNING: force reload - Could not read the worksheet "
                   f"({self.worksheet})."))
            self.data = None

    def __str__(self) -> str:
        return f"Worksheet: {self.worksheet}\ndata: {type(self.data)}"
    
    def update_gsheet(self) -> None:
        self.__connection.update(worksheet = self.worksheet, data = self.data)

    def change_worksheet(self, worksheet : str) -> None:
        self.worksheet = worksheet
        self.force_reload()

    def filter_calendar_per_user_and_date(self, user : str = "/") -> pd.DataFrame:
        calendar = self.data.copy()
        # Transform the "Deadline" column (str) to Timestamp to be able to use 
        # the < operator
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)

        # Fetch the IDs for the rows corresponding to tasks which due date are
        # nigh
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

        # Filter the calendar
        calendar_filtered = calendar.loc[np.isin(calendar["ID"], selected_IDs), :]
        # Sort the calendar per date
        calendar_filtered = calendar_filtered.sort_values(["Deadline"], ascending=True)
        return calendar_filtered