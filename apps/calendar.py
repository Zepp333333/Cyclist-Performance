#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import calendar

from dash_table import DataTable, FormatTemplate, Format
import pandas as pd
from app import app
from IO import DataWrapper
import dash_bootstrap_components as dbc
from datetime import date, timedelta

# todo offload below to constants
WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def day_of_week_to_str(day_of_week: int) -> str:
    return WEEK_DAYS[day_of_week]

def datetime_to_monthdate(dt):
    return dt.strftime("%b, %d")


def get_month_template(year: int, month: int):
    days = [d for d in calendar.Calendar(calendar.firstweekday()).itermonthdates(year, month)]
    return [({day_of_week_to_str(d.weekday()): datetime_to_monthdate(d) for d in days[i:i + 7]}) for i in range(0, len(days), 7)]


layout = DataTable(
    id="calendar",
    data=get_month_template(2021, 1),
    columns=[{'id': d, 'name': d} for d in WEEK_DAYS],
    page_size=3,
    page_current=0,
    virtualization=True,
    fixed_rows={'headers': True},
    style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
    style_table={'height': 300},  # default is 500,
)
