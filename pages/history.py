import pandas as pd
import streamlit as st

from pkg import render_history
st.write("# History")

calendar = pd.read_csv("./data/calendar.csv").sort_values("Deadline",ascending=False)
for iRow in range(len(calendar)):
    st.write(render_history(calendar.iloc[iRow]), unsafe_allow_html=True)