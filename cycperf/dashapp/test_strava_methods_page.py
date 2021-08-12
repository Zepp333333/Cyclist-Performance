#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash_table import DataTable


def make_layout():
    layout = html.Div([

        dcc.ConfirmDialog(
            id='confirm',
            message="Please authorize the application in Strava to proceed",
        ),
        html.Div([
            # first row
            html.Div(children=[
                # first column of first row
                html.Div(children=[
                    html.Button('Get Athlete',
                                id='btn_get_athlete',
                                n_clicks=0,
                                className='btn btn-primary'),
                ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

                # second column of first row
                html.Div(children=[
                    html.Div(
                        id='get_athlete_output',
                        style={'whiteSpace': 'pre-line',
                               'maxHeight': '400px',
                               'overflow': 'scroll',
                               'border': '2px black solid',
                               'display': 'inline-block'},
                    )
                ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'})
            ], className='row'),

            # Second row
            html.Div(children=[
                # first column of second row
                html.Div(children=[
                    html.Button('Get Activities',
                                id='btn_get_activities',
                                n_clicks=0,
                                className='btn btn-primary'),
                ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

                # second column of second row
                html.Div(children=[
                    html.Div(
                        id='get_activities_output',
                        style={'whiteSpace': 'pre-line',
                               'maxHeight': '400px',
                               'overflow': 'scroll',
                               'border': '2px black solid',
                               'display': 'inline-block'},
                    )
                ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'})
            ],
                className='row')
        ])
    ])
    return layout


def json_to_list(json):
    names = [e.name for e in json]
    return [{'activity': n} for n in names]


def make_table(data):
    table = DataTable(
        id="data",
        columns=[{'id':'activity', 'name':'name'}],
        data=json_to_list(data),
        page_size=10,
        page_current=0,
        virtualization=True,
        fixed_rows={'headers': True},
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
        style_table={'height': 300},  # default is 500,
    )
    return table


