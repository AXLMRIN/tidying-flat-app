from .ALLUSERSORTASKS import User
from .TASK import Task
import pandas as pd

STATUS_COLOR = {
    "DONE" : "#6a994e",
    "TODO" : "#168aad",
    "SKIPPED" : "#dad7cd"
}

def render_history(entry : pd.Series) -> str:
    entry : dict = entry.to_dict()
    
    try:
        status_color = STATUS_COLOR[entry["Status"]]
    except:
        status_color = "grey"

    if entry["Deadline"] < pd.Timestamp.today():
        font_color = "#c1121f"
    else:
        font_color = "#252630"

    background = (
        "margin: 2px; border-radius: 15px; padding: 2px;"
       f"background-color: rgba(255,255,255,0.7); border: 4px solid {status_color};"
       "display: flex; flex-direction: column; justify-content: space-between;"
       "align-items: center; flex-wrap: nowrap;"
    )
    title_frame = (
        "display: flex; flex-direction: row; flex-wrap: nowrap; "
        "justify-content: space-between;"
    )
    task_name = (
        "font-weight: bold;"
        "margin: 1px; border-radius: 5px; padding:3px;"
       f"color: {font_color}; font-size: large; text-align:center;"
        "flex: 0 1 auto;"
    )
    user_name = (
        "margin: 1px; border-radius: 5px; padding:3px;"
       f"color: {font_color}; font-size: large; text-align:center;"
        "flex: 0 1 auto;"
    )
    deadline_name = (
        "margin: 1px; border-radius: 5px; padding:3px;"
       f"color: {font_color}; font-size: small; text-align:center;"
        "flex: 0 1 auto;"
    )

    return_str = f'''<div style="{background}">
        <div style="{title_frame}">
            <p style="{task_name}">{entry["Task"]}</p>
            <p style="{user_name}">{entry["User"]}</p>
        </div>
        <p style="{deadline_name}">{pd.Timestamp(entry["Deadline"]).strftime("%Y-%m-%d")}</p>
    </div>'''
    return return_str