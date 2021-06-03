#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import datetime

import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from app import app
from IO import DataWrapper
import dash_bootstrap_components as dbc
from datetime import date, timedelta

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

PAGE_SIZE = 5
WEEK_DAYS = []
for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
    WEEK_DAYS.append({'id': day, 'name': day})


s = pd.date_range(start='2015-01-01', end='2030-12-31').to_series()
df = pd.DataFrame({"date": s})
df["day"] = s.dt.day_of_week
df["week"] = s.dt.isocalendar().week
df["month"] = [m.month for m in s]
df["year"] = s.dt.isocalendar().year
cal = df.pivot(columns="day", index=["year", "month", "week"]).reset_index()


def get_year(dataframe, year):
    return dataframe[dataframe["year"] == year]


def get_month(dataframe, year, month):
    return get_year(dataframe, year)[dataframe["month"] == month]


def get_week(dataframe, year, week):
    return get_year(dataframe, year)[dataframe["week"] == week]

# def create_date_table2(start='2015-01-01', end='2030-12-31'):
#     df = pd.DataFrame({"Date": pd.date_range(start, end)})
#     df["Day"] = df.Date.dt.day_name()
#     df["Week"] = df.Date.dt.isocalendar().week
#     df["Quarter"] = df.Date.dt.quarter
#     df["Year"] = df.Date.dt.year
#     df["Year_half"] = (df.Quarter + 1) // 2
#     return df
#
#
# df = create_date_table2()


layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=15,
    page_current=15,
    virtualization=True,
    fixed_rows={'headers': True},
    style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
    style_table={'height': 300}, # default is 500,
)


def monday_of_calendarweek(year, week_num) -> datetime.date:
    first = date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + timedelta(days=base - first.isocalendar()[2] + 7 * (week_num - 1))


def display_week(year, week_num) -> dash_table.DataTable:
    monday = monday_of_calendarweek(year, week_num)
    week = [monday + timedelta(d) for d in range(6)]
    week_dict = []
    for col, dt in zip(WEEK_DAYS, week):
        week_dict.append({col['id']: dt})
    print(week_dict)

    layout = dash_table.DataTable(
        data=week_dict,
        columns=WEEK_DAYS,
        page_size=15,
        page_current=15,
        virtualization=True,
        fixed_rows={'headers': True},
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
        style_table={'height': 300},  # default is 500,
    )
    return layout


# layout = display_week(2021, 26)

# layout = dash_table.DataTabledf(
# #     id='datatable-paging',
# #     columns=[
# #         {"name": i, "id": i} for i in sorted(df.columns)
# #     ],
# #     page_current=0,
# #     # page_size=PAGE_SIZE,
# #     # page_action='custom',
# #     virtualization=True,
# #     fixed_rows={'headers': True},
# #     style_cell={'midWidth': 95, 'width': 95, 'maxWidth': 95},
# #     style_table={'height', 300}
# # )
#
# # layout = dash_table.DataTable(
# #     data=df.to_dict('records'),
# #     columns=[{'id': c, 'name': c} for c in df.columns],
# #     page_size=15,
# #     page_current=15,
# #     virtualization=True,
# #     fixed_rows={'headers': True},
# #     style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
# #     style_table={'height': 300}, # default is 500,
# #     class_name='table table-striped',
# # )
#
# # layout = dbc.Table.from_dataframe(
# #     df[0:100],
# #     striped=True,
# #     bordered=True,
# #     hover=True,
# #     size='sm',
# #     responsive=True,
# # )


# @app.callback(
#     Output('datatable-paging', 'data'),
#     Input('datatable-paging', "page_current"),
#     Input('datatable-paging', "page_size"))
# def update_table(page_current, page_size):
#     return df.iloc[
#            page_current * page_size:(page_current + 1) * page_size
#            ].to_dict('records')
