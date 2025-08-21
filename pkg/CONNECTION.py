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
