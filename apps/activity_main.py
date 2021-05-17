#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import pathlib


from app import app
from Data import DataWrapper
from Graphs import CustomFigure



# owner: shivp Kaggle. Source: https://data.mendeley.com/datasets
# dataset was modified. Original data: https://www.kaggle.com/shivkp/customer-behaviour

dw = DataWrapper()
df = dw.get_activity(activity_id='ride.csv')

fig = CustomFigure(
        chart_type='Scatter',
        data_frame=df,
        index_col='time',
        data_series=['watts', 'heartrate', 'cadence']
    )
fig = fig.get_fig()

layout = html.Div([
    dcc.Graph(id='my-fig', figure=fig),
])


# @app.callback(
#     Output(component_id='my-fig', component_property='figure'),
#     Input(component_id='my-fig', component_property='relayoutData'),
#     State(component_id='my-fig', component_property='figure')
# )
# def display_value(inpt, state):
#     fig = CustomFigure(
#         chart_type='Scatter',
#         data_frame=df,
#         index_col='time',
#         data_series=['watts', 'heartrate', 'cadence']
#     )
#     fig = fig.get_fig()
#     return fig
