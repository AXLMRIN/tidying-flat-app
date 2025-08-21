import streamlit as st
from streamlit_gsheets import GSheetsConnection

class Connection:
    def __init__(self, worksheet : str):
        # initialise variables
        self.worksheet = worksheet
        self.__connection = st.connection("gsheets", type = GSheetsConnection)
        # read the data
        self.data = self.__connection.read(worksheet = worksheet)

    def force_reload(self):
        self.data = self.__connection.read(worksheet = self.worksheet)