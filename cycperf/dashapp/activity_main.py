#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
import dash_core_components as dcc
import dash_html_components as html
from middleware import Activity

from IO import DataWrapper
from middleware import activity_wrapper
from .utils.scatter_drawer import ScatterDrawer


dw = DataWrapper()
df = dw.get_activity(activity_id='ride.csv')
mock_up_ride = Activity(activity_id=1, name='My ride', df=df)


def _make_layout(activity):
    fig = ScatterDrawer(
        activity=activity,
        index_col='time',
        series_to_plot=['watts', 'heartrate', 'cadence'],
    )
    layout = html.Div([
        # html.H1(current_user['name']),
        html.Button('Create Interval', id='create_interval', n_clicks=0, className="btn btn-primary"),
        dcc.Graph(id='my-fig', figure=fig.get_fig()),
    ])
    return layout


def make_layout(user_id=None, activity_id=None):
    if not user_id or not activity_id:
        return _make_layout(mock_up_ride)
    return _make_layout(activity_wrapper.get_users_last_activity(user_id))



