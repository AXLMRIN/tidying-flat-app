import pandas as pd
import streamlit as st

from pkg import render_history, read_data

calendar = read_data("Calendar")

st.write("# History")

cols = st.columns(4)
for iRow in range(len(calendar)):
    cols[iRow%4].write(render_history(calendar.iloc[iRow]), unsafe_allow_html=True)
    cols[iRow%4].button(label = "", icon = ":material/edit:", key = f"edit-{iRow}", 
                        use_container_width = True, on_click=test, 
                        args=[calendar.iloc[iRow]["ID"]])