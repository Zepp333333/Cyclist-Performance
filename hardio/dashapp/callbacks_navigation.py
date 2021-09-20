#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_login import current_user

from hardio.dashapp import UserConfig, activity_main, calendar, test_strava_methods_page

from iobrocker import IO


def register_navigation_callbacks(dash_app: dash.Dash) -> None:
    @dash_app.callback(
        Output(component_id="page-content", component_property="children"),
        Output(component_id="username_placeholder", component_property="children"),
        Input(component_id="url", component_property="pathname"),
        State(component_id="user_config", component_property="data"),
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
            return [
                       calendar.make_layout(current_user.id, config),
                   ], [current_user.username]
        elif pathname == "/application/activity":
            return [
                       activity_main.make_layout(user_id=current_user.id, activity_id=None, config=config)
                   ], [current_user.username]
        elif "/application/activity/" in pathname:
            activity_id = pathname.split("/")[-1]
            return [
                       activity_main.make_layout(user_id=current_user.id, activity_id=activity_id, config=config)
                   ], [current_user.username]
        elif pathname == "/application/test_strava":
            return [
                       html.H1("Activity", style={"textAlign": "center"}),
                       html.H2(f"Current user id: {current_user.id}"),
                       test_strava_methods_page.make_layout()
                   ], [current_user.username]
        elif "/application/test" in pathname:
            activity_id = pathname.split("/")[-1]
            return [
                       html.H1("test page", style={"textAlign": "center"}),
                       html.H2(activity_id)
                   ], [current_user.username]

        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not Found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized...")
            ]
        )
