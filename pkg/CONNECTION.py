import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

from . import ALLUSERS, ALLTASKS

class Connection:
    def __init__(self, worksheet : str) -> None:
        print("Creation of the \"Connection\" object.")
        # initialise variables
        self.worksheet = "Calendar"
        self.__connection = st.connection("gsheets", type = GSheetsConnection)
        print(f"Loading the dataframe ({self.worksheet})")
        try:
            # read the data
            self.data : pd.DataFrame|None= \
                self.__connection.read(worksheet = self.worksheet)
            print(f"Success (type data: {type(self.data)})")
        except:
            print("Loading failed, data = None ")
            self.data : pd.DataFrame|None = None
        # generate new tasks to the calendar
        self.generate_new_tasks_to_calendar()
    
    def generate_new_tasks_to_calendar(self) -> None:
        """generate calendar for the next month"""
        today = pd.Timestamp.now()
        # Retrieve the calendar
        calendar = self.data.copy()
        # Sort the values so that the low index (ie 0) is the more recent
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)
        calendar = calendar.sort_values("Deadline", ascending = False) 

        tasks_were_added = False
        for _, task in ALLTASKS.data.iterrows():
            task_name = task["Name"]
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
            next_occurence = last_occurence + pd.Timedelta(weeks = task["Frequency"])

            while next_occurence < today + pd.Timedelta(weeks = 4):
                if not tasks_were_added: tasks_were_added = True

                calendar = pd.concat(
                    [
                        calendar,
                        pd.DataFrame({
                            "ID" : [len(calendar) + 1],
                            "Task" : [task_name],
                            "Status" : ["TODO"],
                            "Deadline" : [next_occurence.strftime("%Y-%m-%d")],
                            "User" : ["/"]
                        })
                    ], 
                    ignore_index=True
                )
                next_occurence = next_occurence + pd.Timedelta(weeks = task["Frequency"])
        
        if tasks_were_added:
            self.data = calendar.copy()
            self.update_gsheet()

    def force_reload(self) -> None:
        print(f"Force loading the dataframe ({self.worksheet})")
        try:
            self.data = self.__connection.read(worksheet = self.worksheet, ttl = 1)
            print(f"Success (type data: {type(self.data)})")
        except:
            print("Loading failed, data = None ")
            self.data = None

    def __str__(self) -> str:
        return f"Worksheet: {self.worksheet}\ndata: {type(self.data)}"
    
    def update_gsheet(self) -> None:
        print("Updating the google sheet")
        try:
            self.__connection.update(worksheet = self.worksheet, data = self.data)
            print(f"Success updating ({self.worksheet})")
        except:
            print(f"Failed updating ({self.worksheet})")

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
    
    def get_all_history(self, user : str = "/") -> pd.DataFrame:
        calendar = self.data.copy()
        # Transform the "Deadline" column (str) to Timestamp to be able to use 
        # the < operator
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)

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

        # Filter the calendar
        calendar_filtered = calendar.loc[np.isin(calendar["ID"], selected_rows_user), :]
        # Sort the calendar per date
        calendar_filtered = calendar_filtered.sort_values(["Deadline"], ascending=True)

        return calendar_filtered
    
    def check(self, id : int) -> None:
        self.data.loc[self.data["ID"]==id,"Status"] = "DONE"
        self.update_gsheet()


    @st.dialog("Edit Task")
    def dialog_edit_task(self, id : int) -> None:
        st.write(f'ID : {id}')
        st.write("## Change Status")

        status_options = ["TODO", "DONE", "SKIPPED"]

        def status_index():
            # retrieve the current status index
            current_status = self.data.loc[self.data["ID"]==id,"Status"].item()
            return status_options.index(current_status)
        
        new_status = st.radio(
            label = "Status",
            options = status_options,
            horizontal = True,
            index = status_index()
        )
        st.write("## Change user")
        current_user = self.data.loc[self.data["ID"]==id,"User"].item()
        st.write(f"Current user : {current_user}")
        user_options = ["/", *[user_name for user_name in ALLUSERS.get_all_names()]]
        new_user = st.selectbox(
            label = "User", 
            options = user_options,
            index = user_options.index(current_user),
        )
        if st.button("Submit"):
            # Update data
            if (new_status in status_options)&(new_user in user_options):
                # Safety measures
                self.data.loc[self.data["ID"]==id,"Status"] = new_status
                self.data.loc[self.data["ID"]==id,"User"] = new_user
            st.rerun()