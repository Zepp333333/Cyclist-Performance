#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from iobrocker import IO
from logic import Activity, UserConfig

from . import ConfigForm, ActivityHeader
from .cyclometry import Cyclometry
from .utils import ScatterDrawer, CPPlotter

from ..presenter_config import Tabs as tbs, AppDashIDs as ids, Buttons as btn


class ActivityPresenter:
    def __init__(self, io: IO, context: dict) -> None:
        self.io = io
        self.context = context

    def make_layout(self) -> dash.Dash.layout:
        if 'activity' not in self.context:
            raise Exception

        if ('config' in self.context) and (self.context['config']):
            config = self.context['config']
        else:
            config = self.read_config_from_db(self.io)

        activity_id = self.context['activity']
        if not activity_id:
            last_activity = self.io.get_last_activity()
            self.io.save_activity(last_activity)
            return self._make_layout(last_activity, config)
        return self._make_layout(self.io.get_hardio_activity_by_id(int(activity_id)), config)

    def _make_layout(self, activity: Activity, config: UserConfig = None) -> dash.Dash.layout:
        fig = self.make_figure(activity, config)
        activity_page_content = html.Div([
            ConfigForm().make_configuration_modal(activity, config),
            dcc.Graph(id=ids.activity_main_chart, figure=fig),
            self.make_interval_input_group(),
            self.make_interval_button_group(),
            # dcc.Store inside the app that stores the intermediate value
            dcc.Store(id=ids.activity_store, data=activity.id),  # prepare_activity_for_dcc_store(activity))
            dcc.Store(id=ids.user_config_store, storage_type='session', data=config.to_json())
        ])

        activity_tab = dbc.Card(dbc.CardBody([activity_page_content]), className="mt-3")
        power_tab = dbc.Card(dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(id=ids.activity_cp_chart, figure=CPPlotter().get_cp_fig(activity))
                    ]
                )
            ]
        ), className="mt-3")

        cyclometry_tab = dbc.Card(dbc.CardBody(Cyclometry(self.io, self.context).make_layout()), className="mt-3")

        page_tabs = dbc.Tabs(
            [
                # dbc.Tab(activity_tab, label="Activity", tab_id=ids.activity_tab),
                # dbc.Tab(power_tab, label="Power", tab_id=ids.power_tab),
                dbc.Tab(activity_tab, label=tbs.activity_tab.label, tab_id=tbs.activity_tab.tab_id),
                dbc.Tab(power_tab, label=tbs.power_tab.label, tab_id=tbs.power_tab.tab_id),
                dbc.Tab(cyclometry_tab, label="Cyclometry", tab_id="cyclometry_tab"),

            ],
            id=ids.activity_tabs,
            active_tab=tbs.activity_tab.tab_id
        )

        header = ActivityHeader().make_activity_info_header(activity)
        layout = html.Div(
            [
                header,
                page_tabs,
            ]
        )

        return layout

    def make_figure(self, activity, config: UserConfig) -> ScatterDrawer.get_fig:
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

    def make_interval_button_group(self):
        button_group = dbc.ButtonGroup(
            [
                dbc.Button(btn.create_interval.name, id=btn.create_interval.id, n_clicks=0, className="btn btn-primary"),
                dbc.Button(btn.find_intervals.name, id=btn.find_intervals.id, n_clicks=0, className="btn btn-primary"),
                dbc.Button(btn.delete_intervals.name, id=btn.delete_intervals.id, n_clicks=0, className="btn btn-primary")
            ],
            size="sm",
            className="mr-1",
        )

        return button_group

    def make_interval_input_group(self) -> html:
        input_group = html.Div(
            [
                html.Br(),
                dbc.InputGroup(
                    [
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

    def read_config_from_db(self, io):
        return io.read_user_config()
