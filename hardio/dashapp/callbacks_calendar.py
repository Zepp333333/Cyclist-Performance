#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from dash.dependencies import Input, Output, State
from flask_login import current_user

from hardio.dashapp import calendar


def register_calendar_callbacks(dash_app):
    @dash_app.callback(
        [Output(component_id='calendar_view', component_property='children'),
         Output(component_id='alert-calendar-refresh', component_property='is_open'),
         Output(component_id='refresh_spinner', component_property='children')],
        [Input(component_id='calendar_month_selector', component_property='value'),
         Input(component_id='btn_refresh_activities', component_property='n_clicks')],
        [State(component_id='calendar_month_selector', component_property='value'),
         State(component_id='alert-calendar-refresh', component_property='is_open')],
        prevent_initial_call=True
    )
    def manage_calendar(month_year: str,
                        _btn_refresh: int,
                        month_year_selector_state:
                        str, alert_is_open: bool) -> dash.Dash.layout:
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'btn_refresh_activities.n_clicks':
            calendar.refresh_activities_from_strava(current_user.id, month_year_selector_state)
            return  calendar.make_layout(current_user.id), True, []
        elif ctx.triggered[0]['prop_id'] == 'calendar_month_selector.value':
            return  render_calendar_based_on_user_set_month_year(month_year), False, []


def render_calendar_based_on_user_set_month_year(month_year: str) -> dash.Dash.layout:
    return calendar.make_layout(current_user.id, month_year)
