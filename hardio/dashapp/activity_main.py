#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from iobrocker import IO
from logic import Activity
from . import UserConfig, ConfigForm, ActivityHeader
from .utils import ScatterDrawer, CPPlotter


def make_layout(user_id: int = None, activity_id: int = None, config: UserConfig = None) -> dash.Dash.layout:
    if not user_id:
        return _make_layout(activity=IO(0).build_mock_up_ride())
    if not activity_id:
        io = IO(user_id=user_id)
        last_activity = io.get_last_activity()
        io.save_activity(last_activity)
        return _make_layout(last_activity, config)
    return _make_layout(IO(user_id=user_id).get_hardio_activity_by_id(int(activity_id)), config)


def _make_layout(activity: Activity, config: UserConfig = None) -> dash.Dash.layout:
    fig = make_figure(activity, config)
    page_content = html.Div([
        ConfigForm().make_configuration_modal(activity, config),
        dcc.Graph(id='activity-main-chart', figure=fig),
        make_interval_input_group(),
        make_interval_button_group(),
        # dcc.Store inside the app that stores the intermediate value
        dcc.Store(id="current_activity", data=activity.id),  # prepare_activity_for_dcc_store(activity))
        dcc.Store(id="user_config", storage_type='session', data=config.to_json())
    ])

    activity_tab = dbc.Card(dbc.CardBody([page_content]), className="mt-3")
    power_tab = dbc.Card(dbc.CardBody(
        [
            html.Div(
                [
                    dcc.Graph(id='activity-cp-chart', figure=CPPlotter().get_cp_fig(activity))
                ]

            )

        ]
    ), className="mt-3")

    tabs = dbc.Tabs(
        [
            dbc.Tab(activity_tab, label="Activity", tab_id="Activity"),
            dbc.Tab(power_tab, label="Power", tab_id="Power"),
        ],
        id="activity-tabs",
        active_tab="Activity"
    )

    layout = html.Div(
        [
            ActivityHeader().make_activity_info_header(activity),
            tabs,
        ]
    )

    return layout


def make_figure(activity, config: UserConfig) -> ScatterDrawer.get_fig:
    if config:
        series_to_plot = config.activity_config.charts_to_plot
    else:
        series = {
            'Ride': ['watts', 'heartrate', 'cadence'],
            'VirtualRide': ['watts', 'heartrate', 'cadence'],
            "Run": ['velocity_smooth', 'heartrate', 'cadence']
        }
        series_to_plot = series[activity.type]

    fig = ScatterDrawer(
        activity=activity,
        index_col='time',
        series_to_plot=series_to_plot,
    )
    return fig.get_fig()


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


def make_interval_input_group() -> html:
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
