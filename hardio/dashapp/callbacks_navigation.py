#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_login import current_user

from hardio.dashapp import test_strava_methods_page
from hardio.dashapp.view import CustomDashView
from iobrocker import IO

from presenter import AppDashIDs as ids

def register_navigation_callbacks(dash_app: CustomDashView) -> None:
    @dash_app.callback(
        Output(component_id=ids.page_content, component_property="children"),
        Output(component_id=ids.user_name_placeholder, component_property="children"),
        Input(component_id=ids.url, component_property="pathname"),
        State(component_id="user_config_store", component_property="data"),
    )
    def render_page_content(pathname, user_config) -> dash.Dash.layout:
        """
        Callback defines general structure of an multi-page Dash app.
        :param pathname: string
        :param user_config: json containing user configuration
        :return: layout, username, user_config
        """

        io = IO(current_user.id)
        config = io.read_user_config()

        if pathname == "/application/":
            return [dash_app.presenter.get_calendar()], [current_user.username]
        elif pathname == "/power/":
            return [
                       html.H2(f"Not yet implemented")
                   ], [current_user.username]
        elif pathname == "/fitness/":
            return [
                       html.H2(f"Not yet implemented")
                   ], [current_user.username]
        elif pathname == "/application/activity":
            dash_app.context = {'activity': None}
            return [dash_app.presenter.get_activity()], [current_user.username]
        elif "/application/activity/" in pathname:
            activity_id = pathname.split("/")[-1]
            dash_app.context = {'activity': activity_id}
            return [dash_app.presenter.get_activity()], [current_user.username]
        elif pathname == "/application/test_strava":
            return [
                       html.H1("Activity", style={"textAlign": "center"}),
                       html.H2(f"Current user id: {current_user.id}"),
                       test_strava_methods_page.make_layout()
                   ], [current_user.username]

        # If the user tries to reach a different page, return a 404 message
        return dbc.Card(
            [
                html.H1("404: Not Found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized...")
            ]
        ), [current_user.username]
