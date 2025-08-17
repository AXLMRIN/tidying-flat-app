import streamlit as st
from streamlit_gsheets import GSheetsConnection

from pkg import CONNECTION, read_data

st.write("# TEST Page")


calendar = "MT"

if st.button(label = "Reload"):
    calendar = CONNECTION.read(worksheet = "Calendar")
if st.button(label = "Force Reload"):
    calendar = CONNECTION.read(worksheet = "Calendar", ttl = 1) 

st.write(calendar)