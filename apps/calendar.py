#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import datetime

import dash
from dash.dependencies import Input, Output
from dash_table import DataTable, FormatTemplate, Format
import pandas as pd
from app import app
from IO import DataWrapper
import dash_bootstrap_components as dbc
from datetime import date, timedelta

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

PAGE_SIZE = 5
WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
#     WEEK_DAYS.append({'id': day, 'name': day})




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
    df = get_year(dataframe, year)[dataframe["month"] == month]
    for i in range(3, 10):
        df.rename(columns={df.columns[i][1]: WEEK_DAYS[i - 3]}, inplace=True)
    df.columns = [' '.join(col).strip().replace('date ', '') for col in df.columns.values]
    for day in WEEK_DAYS:
        df[day] = pd.DatetimeIndex(df[day]).strftime("%d")

    return df


def get_week(dataframe, year, week):
    df = get_year(dataframe, year)[dataframe["week"] == week]
    for i in range(3, 10):
        df.rename(columns={df.columns[i][1]: WEEK_DAYS[i - 3]}, inplace=True)
    df.columns = [' '.join(col).strip().replace('date ', '') for col in df.columns.values]
    for day in WEEK_DAYS:
        df[day] = pd.DatetimeIndex(df[day]).strftime("%d")
    return df

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


week = get_week(cal, 2021, 25)
month = get_month(cal, 2021, 1)
# for i in range(3,10):
#     week.rename(columns={week.columns[i][1]: WEEK_DAYS[i-3]}, inplace=True)
# week.columns = [' '.join(col).strip().replace('date ', '') for col in week.columns.values]

# for day in WEEK_DAYS:
#     week[day] = pd.DatetimeIndex(week[day]).strftime("%d")

# for i in range(0,3):
#     week.rename(columns={week.columns[i][1]: week.columns[i][0]}, inplace=True)

# week.columns = week.columns.get_level_values(0)
# for column in range(3, 10):
#     print(column, week.columns[column])
#     week.rename(columns={week.columns[column]: WEEK_DAYS[column - 3]}, inplace=True)

layout = DataTable(
    data=month.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in week.columns][3:],
    page_size=15,
    page_current=0,
    virtualization=True,
    fixed_rows={'headers': True},
    style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
    style_table={'height': 300}, # default is 500,
)


def monday_of_calendarweek(year, week_num) -> datetime.date:
    first = date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + timedelta(days=base - first.isocalendar()[2] + 7 * (week_num - 1))


def display_week(year, week_num) -> DataTable:
    monday = monday_of_calendarweek(year, week_num)
    week = [monday + timedelta(d) for d in range(6)]
    week_dict = []
    for col, dt in zip(WEEK_DAYS, week):
        week_dict.append({col['id']: dt})
    print(week_dict)

    layout = DataTable(
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
