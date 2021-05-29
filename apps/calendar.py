#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from app import app
from IO import DataWrapper
import dash_bootstrap_components as dbc

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

df[' index'] = range(1, len(df) + 1)

PAGE_SIZE = 5


def create_date_table2(start='2000-01-01', end='2050-12-31'):
    df = pd.DataFrame({"Date": pd.date_range(start, end)})
    df["Day"] = df.Date.dt.day_name()
    df["Week"] = df.Date.dt.isocalendar().week
    df["Quarter"] = df.Date.dt.quarter
    df["Year"] = df.Date.dt.year
    df["Year_half"] = (df.Quarter + 1) // 2
    return df

df = create_date_table2()

# layout = dash_table.DataTabledf(
#     id='datatable-paging',
#     columns=[
#         {"name": i, "id": i} for i in sorted(df.columns)
#     ],
#     page_current=0,
#     # page_size=PAGE_SIZE,
#     # page_action='custom',
#     virtualization=True,
#     fixed_rows={'headers': True},
#     style_cell={'midWidth': 95, 'width': 95, 'maxWidth': 95},
#     style_table={'height', 300}
# )

# layout = dash_table.DataTable(
#     data=df.to_dict('records'),
#     columns=[{'id': c, 'name': c} for c in df.columns],
#     page_size=15,
#     page_current=15,
#     virtualization=True,
#     fixed_rows={'headers': True},
#     style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
#     style_table={'height': 300}, # default is 500,
#     class_name='table table-striped',
# )

# layout = dbc.Table.from_dataframe(
#     df[0:100],
#     striped=True,
#     bordered=True,
#     hover=True,
#     size='sm',
#     responsive=True,
# )

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





# @app.callback(
#     Output('datatable-paging', 'data'),
#     Input('datatable-paging', "page_current"),
#     Input('datatable-paging', "page_size"))
# def update_table(page_current, page_size):
#     return df.iloc[
#            page_current * page_size:(page_current + 1) * page_size
#            ].to_dict('records')
