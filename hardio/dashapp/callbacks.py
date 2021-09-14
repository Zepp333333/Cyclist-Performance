#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import url_for
from flask_login import current_user

from hardio.dashapp import activity_main, calendar, test_strava_methods_page, dash_external_redirect
from iobrocker import IO
from iobrocker import strava_swagger


def register_callbacks(dash_app):


    @dash_app.callback(
        Output(component_id='get_athlete_output', component_property='children'),
        Output('confirm', 'displayed'),
        [Input(component_id='btn_get_athlete', component_property='n_clicks')],
        prevent_initial_call=True
    )
    def get_athlete(_):
        # todo add docstrings
        athlete = strava_swagger.get_athlete()
        if athlete:
            return athlete, False
        else:
            return dash_external_redirect.redirect(url_for('users.strava_login')), True

    @dash_app.callback(
        Output(component_id='get_activities_output', component_property='children'),
        # Output('confirm', 'displayed'),
        [Input(component_id='btn_get_activities', component_property='n_clicks')],
        prevent_initial_call=True
    )
    def get_activities(_):
        # todo add docstrings
        activities = IO(current_user.id).get_activities_from_strava()

        if activities:
            return test_strava_methods_page.make_table(activities), False
        else:
            return dash_external_redirect.redirect(url_for('users.strava_login')), True

    @dash_app.callback(
        Output(component_id="configuration-modal-centered", component_property="is_open"),
        [Input(component_id="btn-configuration", component_property="n_clicks"),
         Input(component_id="btn-close-configuration", component_property="n_clicks")],
        [State(component_id="configuration-modal-centered", component_property="is_open")]
    )
    def toggle_configuration_modal(btn1, btn2, is_open):
        if btn1 or btn2:
            return not is_open
        return is_open

    @dash_app.callback(
        [Output(component_id="user_config", component_property="data"),
         Output(component_id="charts_config_switches-output", component_property="children")],
        Input(component_id="charts_config_switches", component_property="value")
    )
    def get_configuration(switches_value):
        print(switches_value, type(switches_value))
        return switches_value, switches_value
