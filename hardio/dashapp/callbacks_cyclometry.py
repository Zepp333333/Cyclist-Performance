#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
from dash import Input, Output, State
from flask import url_for
from flask_login import current_user

from hardio.dashapp import test_strava_methods_page, dash_external_redirect
from hardio.dashapp.view import CustomDashView
from iobrocker import IO, strava_swagger


def register_cyclometry_callbacks(dash_app: CustomDashView):
    @dash_app.callback(
        [
            Output(component_id="page_content", component_property="children"),
            Output(component_id="cyclometry_config_offcanvas", component_property="is_open"), ],
        [Input(component_id="btn_open_cyclometry_config_offcanvas", component_property="n_clicks"),
         Input(component_id="btn_save_cyclometry_config_offcanvas", component_property="n_clicks"), ],
        [State(component_id="cyclometry_config_offcanvas", component_property="is_open"),
         State(component_id='inpt_AWC', component_property='value'),
         State(component_id='inpt_SWC', component_property='value'),
         State(component_id='inpt_CP', component_property='value'),
         State(component_id='inpt_GP', component_property='value'),
         State(component_id="current_activity_store", component_property="data"),],
        prevent_initial_callbacks=True
    )
    def toggle_cyclometry_offcanvas(btn_open_config, btn_save_config, is_open, awc, swc, cp, gp, current_activity):
        if btn_save_config:
            cm_params = {
                'awc': awc,
                'swc': swc,
                'cp': cp,
                'gp': gp
            }
            dash_app.context = {
                'user': current_user.id,
                'activity': current_activity,
                'cyclometry_params': cm_params
            }
            dash_app.presenter.update_cyclometry_view()

            return dash_app.presenter.get_activity(), not is_open
        if btn_open_config:
            return dash.no_update, not is_open
        return dash.no_update, is_open
