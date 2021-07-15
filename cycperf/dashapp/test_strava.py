#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_core_components as dcc
import dash_html_components as html


def make_layout():
    layout = html.Div([

        dcc.ConfirmDialog(
            id='confirm',
            message="Please authorize the application in Strava to proceed",
        ),

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
        ], className='row')
    ])
    return layout
