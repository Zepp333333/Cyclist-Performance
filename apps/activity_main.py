#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
from middleware import Interval, Activity
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
ride = Activity(name='My ride', df=df)
# ride.add_intervals([
#     Interval(activity=ride, start=200, end=800, title="interval1"),
#     Interval(activity=ride, start=1200, end=2000, title="interval2"),
#     Interval(activity=ride, start=1400, end=2200, title="i3")
# ])

fig = CustomFigure(
    activity=ride,
    chart_type='Scatter',
    index_col='time',
    data_series=['watts', 'heartrate', 'cadence'],
)


layout = html.Div([
    html.Button('Create Interval', id='create_interval', n_clicks=0),
    html.Div(id='container-button', children='Press to create interval'),
    dcc.Graph(id='my-fig', figure=fig.get_fig(),
              # config={'editable': True, 'edits': edits}
              ),
])


@app.callback(
    [Output(component_id='container-button', component_property='children'),
     Output(component_id='my-fig', component_property='figure')],
    [Input(component_id='create_interval', component_property='n_clicks')],
    [State(component_id='my-fig', component_property='relayoutData')],
    prevent_initial_call=True
)
def create_interval(n_clicks, relayout_data):
    interval_range = relayout_data_to_range(relayout_data)
    if interval_range:
        ride.make_interval(*interval_range)

    new_fig = CustomFigure(
        activity=ride,
        chart_type='Scatter',
        index_col='time',
        data_series=['watts', 'heartrate', 'cadence'],
    )
    return f'Interval created. n_clicks = {n_clicks}, relayout= {relayout_data}', new_fig.get_fig()


def relayout_data_to_range(relayout_data: dict) -> tuple[int, int]:
    try:
        return int(relayout_data['xaxis.range[0]']), int(relayout_data['xaxis.range[1]'])
    except KeyError:
        return tuple()

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
