#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from dash.dependencies import Input, Output, State

from presenter import AppDashIDs as ids
from presenter import Buttons as btn


def register_calendar_callbacks(dash_app):
    @dash_app.callback(
        [Output(component_id=ids.calendar, component_property='children'),
         Output(component_id=ids.calendar_refresh_alert, component_property='is_open'),
         Output(component_id=ids.spinner, component_property='children')],
        [Input(component_id=ids.calendar_month_selector, component_property='value'),
         Input(component_id=btn.refresh_activities.id, component_property='n_clicks')],
        [State(component_id=ids.calendar_month_selector, component_property='value'),
         State(component_id=ids.calendar_refresh_alert, component_property='is_open')],
        prevent_initial_call=True
    )
    def manage_calendar(month_year: str,
                        _btn_refresh: int,
                        month_year_selector_state:
                        str, alert_is_open: bool) -> dash.Dash.layout:

        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == f"{btn.refresh_activities.id}.n_clicks":
            dash_app.context = {'action': 'refresh', 'month_year': month_year_selector_state}
            return dash_app.presenter.get_calendar(), True, []
        elif ctx.triggered[0]['prop_id'] == f"{ids.calendar_month_selector}.value":
            dash_app.context = {'action': 'change_view', 'month_year': month_year}
            return dash_app.presenter.get_calendar(), False, []
