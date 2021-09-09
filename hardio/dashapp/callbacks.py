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


def register_callbacks(dashapp):
    @dashapp.callback(Output(component_id="page-content", component_property="children"),
                      Output(component_id="username_placeholder", component_property="children"),
                      Input(component_id="url", component_property="pathname")
                      )
    def render_page_content(pathname) -> dash.Dash.layout:
        """
        Callback defines general structure of an multi-page Dash app.
        :param pathname: string
        :return: layout
        """
        if pathname == "/application/":
            return [
                       calendar.make_layout(current_user.id),
                   ], [current_user.username]
        elif pathname == "/application/activity":
            return [
                       activity_main.make_layout(user_id=current_user.id, activity_id=None)
                   ], [current_user.username]
        elif "/application/activity/" in pathname:
            activity_id = pathname.split("/")[-1]
            return [
                       activity_main.make_layout(current_user.id, activity_id)
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


    # @dashapp.callback(
    #     Output(component_id='my-fig', component_property='figure'),
    #     [Input(component_id='find_intervals', component_property='n_clicks'),
    #      Input(component_id='interval_length', component_property='value'),
    #      Input(component_id='how_many_to_find', component_property='value'),
    #      Input(component_id='interval_power', component_property='value'),
    #      Input(component_id='interval_tolerance', component_property='value'),
    #      Input(component_id='current_activity', component_property='data')],
    #     prevent_initial_call=True
    # )
    # def find_intervals(n_clicks: int,
    #                    interval_length: int,
    #                    how_many_to_find: int,
    #                    interval_power: int,
    #                    interval_tolerance: int,
    #                    data: int):
    #     """
    #     Finds intervals in activity based on provided parameters
    #     :param n_clicks: number of create_interval button clicks
    #     :param interval_length - length of interval in seconds
    #     :param how_many_to_find - how many intervals to find
    #     :param interval_power: power to look for
    #     :param interval_tolerance - tolerance in % to power intervals to look for
    #     :param data: dcc.store containing integer id of current activity
    #     :return: go.Figure
    #     """
    #     ctx = dash.callback_context
    #     if not ctx.triggered[0]['prop_id'] == 'find_intervals.n_clicks':
    #         return dash.no_update
    #
    #     if not interval_length or interval_length == 0:
    #         interval_length = 300
    #     if not how_many_to_find or how_many_to_find == 0:
    #         how_many_to_find = 5
    #     if not interval_tolerance or interval_tolerance == 0:
    #         interval_tolerance = 0.2
    #     else:
    #         interval_tolerance /= 100
    #     if not interval_power or interval_power == 0:
    #         interval_power = None
    #
    #     io = IO(current_user.id)
    #     activity = io.get_hardio_activity_by_id(int(data))
    #     found_intervals = activity.find_intervals(length=interval_length,
    #                                               count=how_many_to_find,
    #                                               power=interval_power,
    #                                               tolerance=interval_tolerance)
    #     activity.add_intervals(found_intervals)
    #     io.save_activity(activity)
    #
    #     from .utils.scatter_drawer import ScatterDrawer
    #
    #     new_fig = ScatterDrawer(
    #         activity=activity,
    #         index_col='time',
    #         series_to_plot=['watts', 'heartrate', 'cadence'],
    #     )
    #     return new_fig.get_fig()

    @dashapp.callback(
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

    @dashapp.callback(
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

    # def get_athlete(_):
    #         athlete = strava_swagger.get_athlete()
    #         if athlete:
    #             return strava_swagger.get_athlete(), False
    #         else:
#             return '', True

# @dashapp.callback(
#        Output(component_id='my-fig', component_property='figure'),
#        [Input(component_id='create_interval', component_property='n_clicks')],
#        [State(component_id='my-fig', component_property='relayoutData')],
#        prevent_initial_call=True
#    )
#    def create_interval(n_clicks, relayout_data):
#
#        from .activity_main import ride
#        from .utils.scatter_drawer import ScatterDrawer
#
#        ctx = dashapp.callback_context
#        if ctx.triggered[0]['prop_id'] == 'create_interval.n_clicks':
#            interval_range = relayout_data_to_range(relayout_data)
#            if interval_range:
#                ride._make_interval(*interval_range)
#
#            new_fig = ScatterDrawer(
#                activity=ride,
#                index_col='time',
#                series_to_plot=['watts', 'heartrate', 'cadence'],
#            )
#            return new_fig.get_fig()
#
#    def relayout_data_to_range(relayout_data: dict) -> tuple[int, int]:
#        try:
#            if len(relayout_data) == 1:
#                return int(relayout_data['xaxis.range'][0]), int(relayout_data['xaxis.range'][1])
#            else:
#                result = [int(v) for v in relayout_data.values()]
#                return result[0], result[1]
#        except KeyError:
#            return tuple()
