#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from iobrocker import IO
from logic import Activity
from .utils import ScatterDrawer


def make_layout(user_id=None, activity_id=None) -> dash.Dash.layout:
    if not user_id:
        return _make_layout(user_id=0, activity=IO(0).build_mock_up_ride())
    if not activity_id:
        io = IO(user_id=user_id)
        last_activity = io.get_last_activity()
        io.save_activity(last_activity)
        return _make_layout(user_id, last_activity)
    return _make_layout(user_id, IO(user_id=user_id).get_hardio_activity_by_id(int(activity_id)))


def _make_layout(user_id: int, activity: Activity) -> dash.Dash.layout:
    series_to_plot = {
        'Ride': ['watts', 'heartrate', 'cadence'],
        'VirtualRide': ['watts', 'heartrate', 'cadence'],
        "Run": ['velocity_smooth', 'heartrate', 'cadence']
    }

    fig = ScatterDrawer(
        activity=activity,
        index_col='time',
        series_to_plot=series_to_plot[activity.type],
    )
    page_content = html.Div([
        dcc.Graph(id='my-fig', figure=fig.get_fig()),
        make_interval_input_group(),
        make_interval_button_group(),
        # dcc.Store inside the app that stores the intermediate value
        dcc.Store(id='current_activity', data=activity.id)  # prepare_activity_for_dcc_store(activity))
    ])

    activity_tab = dbc.Card(dbc.CardBody([page_content]), className="mt-3")
    power_tab = dbc.Card(dbc.CardBody([html.P("This is tab 2", className="card-text")]), className="mt-3")

    tabs = dbc.Tabs(
        [
            dbc.Tab(activity_tab, label="Activity"),
            dbc.Tab(power_tab, label="Power"),
        ]
    )

    layout = html.Div(
        [
            make_activity_info_header(activity),
            tabs,
        ]
    )

    return layout


def make_activity_info_header(activity: Activity):
    line1 = dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    dbc.ListGroupItemHeading(activity.name, style={'font-size': '1rem'}),
                    dbc.ListGroupItemText(activity.date),
                    dbc.ListGroupItemText("text2"),
                ]
            ),
            dbc.ListGroupItem(
                [
                    dbc.ListGroupItemHeading("Power", style={'font-size': '1rem'}),
                    dbc.ListGroupItemText(f"Avg power: {activity.intervals[0].avg_power} text"),
                    dbc.ListGroupItemText(f"Max power: {activity.intervals[0].max_power}"),

                ]
            ),
            dbc.ListGroupItem(
                [
                    dbc.ListGroupItemHeading("HR", style={'font-size': '1rem'}),
                    dbc.ListGroupItemText(f"Avg HR: {activity.intervals[0].avg_hr}"),
                    dbc.ListGroupItemText(f"Max HR: {activity.intervals[0].max_hr}"),

                ]
            ),
        ],
        horizontal=True,
        className="mb-1",
        style={'font-size': '0.8rem'},
    )

    line2 = dbc.ListGroup(
        [

        ]
    )

    list_group = html.Div(
        [
            line1,
            line2,
        ]
    )
    return list_group


def make_interval_button_group():
    button_group = dbc.ButtonGroup(
                [
                    dbc.Button('Create Interval', id='create_interval', n_clicks=0, className="btn btn-primary"),
                    dbc.Button('Find Intervals', id='find_intervals', n_clicks=0, className="btn btn-primary"),
                    dbc.Button('Delete Intervals', id='delete_intervals', n_clicks=0, className="btn btn-primary")
                ],
                size="sm",
                className="mr-1",
            )

    return button_group


def make_interval_input_group():
    input_group = html.Div(
        [

            html.Br(),
            dbc.InputGroup(
                [
                    # dbc.InputGroupAddon("Small", addon_type="prepend"),
                    dbc.Input(id='interval_duration', type="number", placeholder='Set interval length'),
                    dbc.Input(id='how_many_to_find', type="number", placeholder='How many to find'),
                    dbc.Input(id='interval_power', type="number", placeholder='Interval Power, wt'),
                    dbc.Input(id='interval_tolerance', type="number", placeholder='Tolerance %'),
                 ],
                size="sm",
            ),

        ]
    )
    return input_group
