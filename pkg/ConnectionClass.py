import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class Connection:
    def __init__(self) -> None:
        print("Creation of the \"Connection\" object.")
        # initialise variables
        self.calendar_worksheet = "Calendar"
        self.tasks_worksheet = "Tasks"
        self.users_worksheet = "Users"
        self.tasks, self.users, self.calendar = (None,) * 3
        self.user_names = ["/"]
        self.__connection = st.connection("gsheets", type = GSheetsConnection)
        
        # Load the tasks
        print(f"Loading the dataframe ({self.tasks_worksheet})")
        try:
            # read the data
            self.tasks : pd.DataFrame = \
                self.__connection.read(worksheet = self.tasks_worksheet)
            print(f"Success (type data: {type(self.tasks)})")
        except:
            print("Loading failed, tasks = None ")
        
        # Load the Users
        print(f"Loading the dataframe ({self.users_worksheet})")
        try:
            # read the data
            self.users : pd.DataFrame = \
                self.__connection.read(worksheet = self.users_worksheet)
            print(f"Success (type data: {type(self.users)})")
            self.user_names += self.users["Name"].to_list()
        except:
            print("Loading failed, users = None ")

        # Load the calendar
        print(f"Loading the dataframe ({self.calendar_worksheet})")
        try:
            # read the data
            self.calendar : pd.DataFrame|None= \
                self.__connection.read(worksheet = self.calendar_worksheet)
            print(f"Success (type data: {type(self.calendar)})")
            # generate new tasks to the calendar
            self.generate_new_tasks_to_calendar()
        except:
            print("Loading failed, calendar = None ")
    
    def __crop_task_name(self, task_name: str)->str:
        "Salle de bain (haut) -> SDBH"
        task_name_words = task_name.\
            replace("/","").\
            replace("(","").\
            replace(")","").\
            split(" ")
        return "".join([word[0].capitalize() for word in task_name_words if word !=""])
            
    def generate_new_tasks_to_calendar(self) -> None:
        """generate calendar for the next month"""
        today = pd.Timestamp.now()
        # Retrieve the calendar
        calendar = self.calendar.copy()
        # Sort the values so that the low index (ie 0) is the more recent
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)
        calendar = calendar.sort_values("Deadline", ascending = False) 

        tasks_were_added = False
        for _, task in self.tasks.iterrows():
            task_name = task["Name"]
            sub_calendar = calendar.loc[calendar["Task"] == task_name, :]
            if len(sub_calendar) == 0: 
                # The task does not appear in the history
                last_occurence = today
                last_user = input(f"{self.user_names} Enter user name for the new task ({task_name})\n")
            else:
                # Fetch the last iteration:
                last_occurence = pd.Timestamp(sub_calendar.iloc[0]["Deadline"])
                last_user = sub_calendar.iloc[0]["User"]
            # Reset the time
            last_occurence = last_occurence.\
                replace(hour = 0, minute = 0, second = 0, microsecond = 0)
            # Add events for the next month
            next_occurence = last_occurence + pd.Timedelta(weeks=task["Frequency"])
            next_user = self.__choose_user(task["User pool"], last_user)
            task_number = len(sub_calendar)+1

            while next_occurence < today + pd.Timedelta(weeks = 4):
                if not tasks_were_added: tasks_were_added = True

                # Create a new row and add it to the calendar
                new_row = pd.DataFrame({
                    "ID" : [f"T-{self.__crop_task_name(task_name)}-{task_number}"],
                    "Task" : [task_name],
                    "Status" : ["TODO"],
                    "Deadline" : [next_occurence], #Timestamp
                    "User" : [next_user]
                })
                calendar = pd.concat([calendar,new_row], ignore_index=True)
                
                # Increment the next occurence
                next_user = self.__choose_user(task["User pool"], next_user)
                next_occurence = next_occurence + pd.Timedelta(weeks = task["Frequency"])
                task_number += 1
        
        if tasks_were_added:
            # Change back the Deadline to strings
            calendar["Deadline"] = calendar["Deadline"].apply(
                lambda timestamp : timestamp.strftime("%Y-%m-%d"))
            self.calendar = calendar.copy()
            self.update_gsheet()
    
    def __choose_user(self, user_pool : str, last_user : str) -> str:
        if user_pool == "/": 
            # User names contains "/" for other purposes, but we don't want it 
            # when assigning tasks
            user_pool = self.user_names[1:]
        else: 
           user_pool = [user_name.replace(" ","") for user_name in user_pool.split(",")]
        try:
            current_index = user_pool.index(last_user)
            next_index = (current_index + 1) % len(user_pool)
            return user_pool[next_index]
        except:
            print((f"ERREUR (__choose_user): {last_user} not in {user_pool}, "
                   f"returned {user_pool[0]}"))
            return user_pool[0]

    def force_reload(self) -> None:
        print(f"Force loading the dataframe ({self.calendar_worksheet})")
        try:
            self.calendar = self.__connection.read(worksheet = self.calendar_worksheet, ttl = 1)
            print(f"Success (type data: {type(self.calendar)})")
        except:
            print("Loading failed, data = None ")
            self.calendar = None

    def __str__(self) -> str:
        return f"Worksheet: {self.calendar_worksheet}\ndata: {type(self.calendar)}"
    
    def update_gsheet(self) -> None:
        print("Updating the google sheet")
        try:
            self.__connection.update(worksheet = self.calendar_worksheet, data = self.calendar)
            print(f"Success updating ({self.calendar_worksheet})")
        except:
            print(f"Failed updating ({self.calendar_worksheet})")

    def change_worksheet(self, worksheet : str) -> None:
        self.calendar_worksheet = worksheet
        self.force_reload()

    def filter_calendar_per_user_and_date(self, user : str = "/") -> pd.DataFrame:
        calendar = self.calendar.copy()
        # Transform the "Deadline" column (str) to Timestamp to be able to use 
        # the < operator
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)

        # Fetch the IDs for the rows corresponding to tasks which due date are
        # nigh
        date_max = pd.Timestamp.now() + pd.Timedelta(weeks = 1, days = 1)
        date_min = pd.Timestamp.now() - pd.Timedelta(days = 1)

        selected_rows_date = (
            calendar.loc[
                (calendar["Deadline"] >= date_min) & 
                (calendar["Deadline"] <= date_max),
                "ID"
            ].
            to_list()
        )

        # Fetch the IDs for the rows corresponding to tasks associated to a specific
        # user, if provided
        if user != "/":
            selected_rows_user = (
                calendar.loc[
                    calendar["User"] == user,
                    "ID"
                ].
                to_list()  
            )
        else:
            # Take them all because of the way we combine the lists, see below
            selected_rows_user = calendar["ID"].to_list()
        
        # Combine IDs from the user and date
        selected_IDs = [ID for ID in selected_rows_date if ID in selected_rows_user]

        # Filter the calendar
        calendar_filtered = calendar.loc[np.isin(calendar["ID"], selected_IDs), :]
        # Sort the calendar per date
        calendar_filtered = calendar_filtered.sort_values(["Deadline"], ascending=True)
        return calendar_filtered
    
    def get_all_history(self, user : str = "/") -> pd.DataFrame:
        calendar = self.calendar.copy()
        # Transform the "Deadline" column (str) to Timestamp to be able to use 
        # the < operator
        calendar["Deadline"] = calendar["Deadline"].apply(pd.Timestamp)

        # Fetch the IDs for the rows corresponding to tasks associated to a specific
        # user, if provided
        if user != "/":
            selected_rows_user = calendar.loc[
                calendar["User"] == user,
                "ID"].\
                to_list()   
        else:
            # Take them all because of the way we combine the lists, see below
            selected_rows_user = calendar["ID"].to_list()

        # Filter the calendar
        calendar_filtered = calendar.loc[np.isin(calendar["ID"], selected_rows_user), :]
        # Sort the calendar per date
        calendar_filtered = calendar_filtered.sort_values(["Deadline"], ascending=True)

        return calendar_filtered
    
    def check(self, id : int) -> None:
        self.calendar.loc[self.calendar["ID"]==id,"Status"] = "DONE"
        self.update_gsheet()

    @st.dialog("Task description")
    def dialog_task_description(self, task_name : str) -> None:
        st.write(task_name)
        st.write(self.tasks.loc[self.tasks["Name"] == task_name,"Description"].item())

    @st.dialog("Edit Task")
    def dialog_edit_task(self, id : int) -> None:
        st.write(f'ID : {id}')
        st.write("## Change Status")

        status_options = ["TODO", "DONE", "SKIPPED"]

        def status_index():
            # retrieve the current status index
            current_status = self.calendar.loc[self.calendar["ID"]==id,"Status"].item()
            return status_options.index(current_status)
        
        new_status = st.radio(
            label = "Status",
            options = status_options,
            horizontal = True,
            index = status_index()
        )
        st.write("## Change user")
        current_user = self.calendar.loc[self.calendar["ID"]==id,"User"].item()
        st.write(f"Current user : {current_user}")
        
        new_user = st.selectbox(
            label = "User", 
            options = self.user_names,
            index = self.user_names.index(current_user),
        )
        if st.button("Submit"):
            # Update data
            if (new_status in status_options)&(new_user in self.user_names):
                # Safety measures
                self.calendar.loc[self.calendar["ID"]==id,"Status"] = new_status
                self.calendar.loc[self.calendar["ID"]==id,"User"] = new_user
            st.rerun()