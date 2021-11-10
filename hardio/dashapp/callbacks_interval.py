#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from dash.dependencies import Input, Output, State
from flask_login import current_user

from hardio.dashapp.view import CustomDashView

from iobrocker import IO
from . import UserConfig

from .activity_main import make_figure


def register_interval_callbacks(dash_app: CustomDashView) -> None:
    @dash_app.callback(
        Output(component_id='activity_main_chart', component_property='figure'),
        [Input(component_id='btn_create_interval', component_property='n_clicks'),
         Input(component_id='btn_find_intervals', component_property='n_clicks'),
         Input(component_id='btn_delete_intervals', component_property='n_clicks'),
         Input(component_id='interval_duration', component_property='value'),
         Input(component_id='how_many_to_find', component_property='value'),
         Input(component_id='interval_power', component_property='value'),
         Input(component_id='interval_tolerance', component_property='value'),
         Input(component_id='current_activity_store', component_property='data')],
        [State(component_id='activity_main_chart', component_property='relayoutData'),
         State(component_id='user_config_store', component_property='data')],
        prevent_initial_call=True
    )
    def manage_intervals(_: int,
                         __: int,
                         ___: int,
                         interval_duration: int,
                         how_many_to_find: int,
                         interval_power: int,
                         interval_tolerance: int,
                         activity_id: int,
                         relayout_data: dict,
                         user_config: dict):
        """
        Creates an interval in current activity based on relayoutData and button click"
        :param n_clicks: number of create_interval button clicks
        :param interval_duration - length of interval in seconds
        :param how_many_to_find - how many intervals to find
        :param interval_power: power to look for
        :param interval_tolerance - tolerance in % to power intervals to look for
        :param activity_id: dcc.store containing integer id of current activity
        :param relayout_data: dict containing ends of a range slider (or user selection on a graph)
        :param user_config: dict containing jsonified UserConfig object
        :return: go.Figure
        """

        config = UserConfig.from_json(user_config)

        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == "btn_create_interval.n_clicks":
            dash_app.context = {
                'user': current_user.id,
                'activity': activity_id,
                'intervals_range': relayout_data,
                'config': config
            }
            return dash_app.presenter.activity_create_intervals_and_refresh_view()


        elif ctx.triggered[0]['prop_id'] == "btn_delete_intervals.n_clicks":
            dash_app.context = {
                'user': current_user.id,
                'activity': activity_id,
                'config': config
            }
            return dash_app.presenter.activity_delete_intervals_and_refresh_view()


        elif ctx.triggered[0]['prop_id'] == "btn_find_intervals.n_clicks":
            dash_app.context = {
                'user': current_user.id,
                'activity': activity_id,
                'config': config,
                'interval_finder_prams': {
                    'duration': interval_duration,
                    'count': how_many_to_find,
                    'power': interval_power,
                    'tolerance': interval_tolerance
                }
            }
            return dash_app.presenter.activity_find_intervals_and_refresh_view()
        return dash.no_update
