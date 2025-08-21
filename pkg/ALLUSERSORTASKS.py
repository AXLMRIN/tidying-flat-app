import os

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class AllUsersOrTasks:
    def __init__(self, worksheet : str) -> None:
        print("Creation of the \"AllUsersOrTasks\" object.")
        self.worksheet = worksheet
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