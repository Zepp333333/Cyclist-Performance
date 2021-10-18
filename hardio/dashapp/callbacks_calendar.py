#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from dash.dependencies import Input, Output, State
from flask_login import current_user

from iobrocker import IO
from . import UserConfig

from .activity_main import make_figure

from hardio.dashapp import UserConfig, activity_main, calendar


def register_calendar_callbacks(dash_app):
    @dash_app.callback(
        Output(component_id='calendar_view', component_property='children'),
        Input(component_id='calendar_month_selector', component_property='value'),
        prevent_initial_call=True
    )
    def get_athlete(calendar_preference: str):
        print(calendar_preference)
        if not calendar_preference:
            return calendar.make_layout(current_user.id)
        m, y = calendar_preference.split(" ")
        month_year = int(m), int(y)
        return calendar.make_layout(current_user.id, month_year)
