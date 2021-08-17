#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_core_components as dcc
import dash_html_components as html

from iobrocker import IO
from middleware import Activity
from .utils import ScatterDrawer


def _make_layout(user_id: int, activity: Activity) -> dash.Dash.layout:
    fig = ScatterDrawer(
        activity=activity,
        index_col='time',
        series_to_plot=['watts', 'heartrate', 'cadence'],
    )
    layout = html.Div([
        html.H1("Activity", style={"textAlign": "center"}),
        html.H2(user_id),
        html.Button('Create Interval', id='create_interval', n_clicks=0, className="btn btn-primary"),
        dcc.Graph(id='my-fig', figure=fig.get_fig()),

        # dcc.Store inside the app that stores the intermediate value
        dcc.Store(id='current_activity', data=activity.id)  # prepare_activity_for_dcc_store(activity))
    ])
    return layout


def make_layout(user_id=None, activity_id=None) -> dash.Dash.layout:
    if not user_id:
        return _make_layout(user_id=0, activity=IO(0).build_mock_up_ride())
    if not activity_id:
        return _make_layout(user_id, IO(user_id=user_id).get_last_activity())
    return _make_layout(user_id, IO().get_activity_by_id(int(activity_id)))



