import pandas as pd

from . import CONNECTION

def update_sheet(data : pd.DataFrame, worksheet : str):
    CONNECTION.update(worksheet = worksheet, data = data)

def read_data(worksheet : str, force : bool = False) -> pd.DataFrame:
    ttl = 1 if force else 3600 
    calendar = CONNECTION.read(worksheet = worksheet, ttl = ttl)
    return calendar