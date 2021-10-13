#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from . import UserConfig, ConfigForm, ActivityHeader
from .utils import ScatterDrawer, CPPlotter

from hardio.dashapp import View


class ActivityView(View):
    def __init__(self):
        self.header = html.Div([])
        self.page_tabs = html.Div([])

    # def make_layout(self, user_id: int = None, activity_id: int = None, config: UserConfig = None) -> dash.Dash.layout:
    #     activity = self.presenter.get_activity(user_id=user_id, activity_id=activity_id)
    #     config = self.presenter.get_config(user_id=user_id, activity_id=activity_id)

    @property
    def page(self) -> dash.Dash.layout:
        layout = html.Div([
            self.header,
            self.page_tabs,
        ])
        return layout

    def make_page_tabs(self, tabs: dict[str, html.Div]):
        tabs_list = []
        for name, tab in tabs.items():
            tabs_list.append(dbc.Tab(tab, label=name, tba_id=name))
        return dbc.Tabs(tabs_list, id="activity-tabs", active_tab="Activity")

    def make_activity_tab(self):
        activity_tab_content = html.Div(
            [
                ConfigForm().make_configuration_modal(activity, config),
                dcc.Graph(id='activity-main-chart', figure=fig),
                make_interval_input_group(),
                make_interval_button_group(),
                # dcc.Store inside the app that stores the intermediate value
                dcc.Store(id="current_activity", data=activity.id),
                dcc.Store(id="user_config", storage_type='session', data=config.to_json())
            ]
        )
        activity_tab = dbc.Card(dbc.CardBody([activity_tab_content]), className="mt-3")
        return activity_tab

    def make_power_tab(self):
        power_tab_content = html.Div([
            dcc.Graph(id='activity-cp-chart', figure=CPPlotter().get_cp_fig(activity))
        ])
        power_tab = dbc.Card(dbc.CardBody([power_tab_content]), className="mt-3")
        return power_tab


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
