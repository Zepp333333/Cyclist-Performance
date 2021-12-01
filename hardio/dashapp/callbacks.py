#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
from dash import Input, Output, State
from flask import url_for
from flask_login import current_user

from hardio.dashapp import test_strava_methods_page, dash_external_redirect
from hardio.dashapp.view import CustomDashView
from iobrocker import IO, strava_swagger


def register_callbacks(dash_app: CustomDashView):
    @dash_app.callback(
        Output(component_id='get_athlete_output', component_property='children'),
        Output('confirm', 'displayed'),
        [Input(component_id='btn_get_athlete', component_property='n_clicks')],
        prevent_initial_call=True
    )
    def get_athlete(_):
        athlete = strava_swagger.get_athlete()
        if athlete:
            return athlete, False
        else:
            return dash_external_redirect.redirect(url_for('users.strava_login')), True

    @dash_app.callback(
        [Output(component_id="page_content", component_property="children"),
         Output(component_id="configuration_modal_centered", component_property="is_open"),
         Output(component_id="user_config_store", component_property="data")
         ],
        [Input(component_id="btn_open_configuration", component_property="n_clicks"),
         Input(component_id="btn_save_configuration", component_property="n_clicks"),
         Input(component_id="btn_close_configuration", component_property="n_clicks"), ],
        [State(component_id="charts_config_switches", component_property="value"),
         State(component_id="configuration_modal_centered", component_property="is_open"),
         State(component_id="current_activity_store", component_property="data")],
        prevent_initial_callbacks=True
    )
    def toggle_configuration_modal(btn_open_config, btn_save_config, btn_close_config, switches_value, is_open,
                                   current_activity):
        if btn_save_config:
            dash_app.context = {
                'user': current_user.id,
                'activity': current_activity,
                'switches': switches_value
            }
            page, config = dash_app.presenter.save_config_and_update_page()
            return page, not is_open, config.to_json()
        if btn_open_config or btn_close_config:
            return dash.no_update, not is_open, dash.no_update
        return dash.no_update, is_open, dash.no_update


    @dash_app.callback(
        Output(component_id='get_activities_output', component_property='children'),
        # Output('confirm', 'displayed'),
        [Input(component_id='btn_get_activities', component_property='n_clicks')],
        prevent_initial_call=True
    )
    def get_activities(_):
        activities = IO(current_user.id).get_activities_from_strava()

        if activities:
            return test_strava_methods_page.make_table(activities), False
        else:
            return dash_external_redirect.redirect(url_for('users.strava_login')), True
