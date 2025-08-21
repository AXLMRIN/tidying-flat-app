from .USER import User
from .TASK import Task
import pandas as pd

STATUS_COLOR = {
    "DONE" : "#6a994e",
    "TODO" : "#168aad",
    "SKIPPED" : "#dad7cd"
}

def render_user(user:User) -> str:
    data = user.get_data()

    style_div = (
        "margin: 5px; border-radius: 15px; padding: 3px;"
        f"background-color: {data["color"]};"
        "display: flex; flex-direction: column; flex-wrap: nowrap;"
        "justify-content: center; align-items: center;"
    )
    style_name = (
        "margin: 1px; width: 90%; border-radius: 5px; padding:3px;"
        "background-color: white; opacity: 0.5;"
        "color: black; font-size: large; text-align:center;"
    )
    style_email = (
        "margin: 1px; width: 90%; border-radius: 5px; padding:3px;"
        "background-color: white; opacity: 0.5;"
        "color: black; text-align:center;"
    )
    style_score = (
        "margin: 1px; width: 90%; border-radius: 5px; padding:3px;"
        "background-color: white; opacity: 0.5;"
        "color: black; font-size: large; text-align:center;"
    )
    return_str = f'''<div style="{style_div}">
    <p style="{style_name}">{data["name"]}</p>
    <p style="{style_email}">{data["email"]}</p>
    <p style="{style_score}">{data["score"]}</p>
    </div>'''
    return return_str

def render_task(task:Task) -> str:
    data = task.get_data()

    style_div = (
        "margin: 5px; border-radius: 15px; padding: 3px;"
        "background-color: grey;"
        "display: flex; flex-direction: row; flex-wrap: nowrap;"
        "justify-content: space-between; align-items: center;"
    )
    style_name = (
        "margin: 1px; width: 30%; border-radius: 5px; padding:3px;"
        "color: black; font-size: large; text-align:center;"
    )
    style_description = (
        "margin: 1px; width: 40%; border-radius: 5px; padding:3px;"
        "color: black; text-align:center;"
    )
    style_frequency = (
        "margin: 1px; width: 30%; border-radius: 5px; padding:3px;"
        "color: black; font-size: large; text-align:center;"
    )
    return_str = f'''<div style="{style_div}">
    <p style="{style_name}">{data["name"]}</p>
    <p style="{style_description}">{data["description"]}</p>
    <p style="{style_frequency}">every {data["frequency"]} week</p>
    </div>'''
    return return_str

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