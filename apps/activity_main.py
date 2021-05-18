#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
from middleware import Interval
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import pathlib

from app import app
from IO import DataWrapper
from graphs import CustomFigure

from plotly.subplots import make_subplots
import plotly.graph_objects as go

dw = DataWrapper()
df = dw.get_activity(activity_id='ride.csv')

fig = CustomFigure(
    chart_type='Scatter',
    data_frame=df,
    index_col='time',
    data_series=['watts', 'heartrate', 'cadence'],
    intervals=[
        Interval(start=200, end=800, title="interval1", df=df.iloc[200:800]),
        Interval(start=2000, end=2500, title="interval2", df=df.iloc[2000:2500]),
    ]
)
fig = fig.get_fig()

# edits = {
#             'annotationPosition': False,
#             'annotationTail': False,
#             'annotationText': False,
#             'axisTitleText': False,
#             'colorbarPosition': False,
#             'colorbarTitleText': False,
#             'legendPosition': False,
#             'legendText': False,
#             'shapePosition': False,
#             'titleText': False
#         }


layout = html.Div([
    html.Button('Create Interval', id='create_interval', n_clicks=0),
    html.Div(id='container-button', children='Press to create interval'),
    dcc.Graph(id='my-fig', figure=fig,
              # config={'editable': True, 'edits': edits}
              ),

])


@app.callback(
    Output(component_id='container-button', component_property='children'),
    [Input(component_id='create_interval', component_property='n_clicks'),],
    [State(component_id='my-fig', component_property='relayoutData')],
    prevent_initial_call=True
)
def create_interval(n_clicks, relayout_data):
    return f'Interval created. n_clicks = {n_clicks}, relayout= {relayout_data}'





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
