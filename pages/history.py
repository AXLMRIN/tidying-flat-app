import pandas as pd
import streamlit as st

from pkg import render_history

calendar = pd.read_csv("./data/calendar.csv").sort_values("Deadline",ascending=False)

st.write("# History")

for iRow in range(len(calendar)):
    st.write(render_history(calendar.iloc[iRow]), unsafe_allow_html=True)