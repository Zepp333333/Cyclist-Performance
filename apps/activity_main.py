#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib

import Data.DataWrapper
from app import app
from Data import DataWrapper as dw

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../Data").resolve()

# owner: shivp Kaggle. Source: https://data.mendeley.com/datasets
# dataset was modified. Original data: https://www.kaggle.com/shivkp/customer-behaviour

data_weapper = dw.DataWrapper()
df = data_weapper.get_activity(DATA_PATH.joinpath('ride.csv'))


layout = html.Div([
    html.H1('General Product Sales', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Payment type", style={"fontSize":"150%"}),
        ], className='six columns'),

    ], className='row'),

    dcc.Graph(id='my-map', figure={}),
])


@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='pymnt-dropdown', component_property='value'),
     Input(component_id='country-dropdown', component_property='value')]
)
def display_value(pymnt_chosen, country_chosen):
    fig = Graphs.CustomFigure(
        chart_type='Scatter',
        data_frame=df,
        index_col='time',
        data_series=['watts', 'heartrate', 'cadence']
    )
    fig = fig.get_fig()
    return fig
