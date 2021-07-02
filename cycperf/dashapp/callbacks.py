#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from cycperf.dashapp import activity_main, calendar
from flask_login import current_user


def register_callbacks(dashapp):
    @dashapp.callback(Output(component_id="page-content", component_property="children"),
                      Output(component_id="username_placeholder", component_property="children"),
                      Input(component_id="url", component_property="pathname")
                      )
    def render_page_content(pathname):
        if pathname == "/application/":
            return [
                html.H1("Home page", style={"textAlign": "center"}),
                calendar.layout
            ], [current_user.username]
        # elif pathname == "/login":
        #     return [
        #         html.H1("Login page", style={"textAlign": "center"}),
        #         IO.strava2.r
        #     ]
        elif pathname == "/application/activity":
            return [
                html.H1("Activity page", style={"textAlign": "center"}),
                html.H2(current_user.id),
                activity_main.make_layout(current_user.id)
            ], [current_user.username]
        elif pathname == "/application/else":
            return [
                html.H1("Something Else page", style={"textAlign": "center"}),
            ], [current_user.username]

        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not Found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized...")
            ]
        )

    @dashapp.callback(
        Output(component_id='my-fig', component_property='figure'),
        [Input(component_id='create_interval', component_property='n_clicks')],
        [State(component_id='my-fig', component_property='relayoutData')],
        prevent_initial_call=True
    )
    def create_interval(n_clicks, relayout_data):

        from .activity_main import ride
        from .utils.scatter_drawer import ScatterDrawer

        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'create_interval.n_clicks':
            interval_range = relayout_data_to_range(relayout_data)
            if interval_range:
                ride.make_interval(*interval_range)

            new_fig = ScatterDrawer(
                activity=ride,
                index_col='time',
                series_to_plot=['watts', 'heartrate', 'cadence'],
            )
            return new_fig.get_fig()

    def relayout_data_to_range(relayout_data: dict) -> tuple[int, int]:
        try:
            if len(relayout_data) == 1:
                return int(relayout_data['xaxis.range'][0]), int(relayout_data['xaxis.range'][1])
            else:
                result = [int(v) for v in relayout_data.values()]
                return result[0], result[1]
        except KeyError:
            return tuple()
