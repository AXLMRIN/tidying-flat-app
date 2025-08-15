from .USER import User
from .TASK import Task
import pandas as pd

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

    style_div = (
        "margin: 5px; border-radius: 15px; padding: 3px;"
        "background-color: grey;"
        "display: flex; flex-direction: row; flex-wrap: nowrap;"
        "justify-content: space-between; align-items: center;"
    )
    style_text = (
        "margin: 1px; width: 20%; border-radius: 5px; padding:3px;"
        "color: black; font-size: large; text-align:center;"
    )

    return_str = f'''<div style="{style_div}">
    <p style="{style_text}">{entry["ID"]}</p>
    <p style="{style_text}">{entry["Task"]}</p>
    <p style="{style_text}">{entry["User"]}</p>
    <p style="{style_text}">{entry["Deadline"]}</p>
    <p style="{style_text}">{entry["Status"]}</p>
    </div>'''
    return return_str