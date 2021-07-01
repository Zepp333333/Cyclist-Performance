#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
import dash_core_components as dcc
import dash_html_components as html
from middleware import Activity
from dash.dependencies import Input, Output, State


# from cycperf import app
from IO import DataWrapper
from .utils.scatter_drawer import ScatterDrawer


dw = DataWrapper()
df = dw.get_activity(activity_id='ride.csv')
ride = Activity(name='My ride', df=df)

fig = ScatterDrawer(
    activity=ride,
    index_col='time',
    series_to_plot=['watts', 'heartrate', 'cadence'],
)

layout = html.Div([
    # html.H1(current_user['name']),
    html.Button('Create Interval', id='create_interval', n_clicks=0, className="btn btn-primary"),
    dcc.Graph(id='my-fig', figure=fig.get_fig()),
])


# @app.callback(
#     Output(component_id='my-fig', component_property='figure'),
#     [Input(component_id='create_interval', component_property='n_clicks')],
#     [State(component_id='my-fig', component_property='relayoutData')],
#     prevent_initial_call=True
# )
# def create_interval(n_clicks, relayout_data):
#     ctx = dash.callback_context
#     if ctx.triggered[0]['prop_id'] == 'create_interval.n_clicks':
#         interval_range = relayout_data_to_range(relayout_data)
#         if interval_range:
#             ride.make_interval(*interval_range)
#
#         new_fig = ScatterDrawer(
#             activity=ride,
#             index_col='time',
#             series_to_plot=['watts', 'heartrate', 'cadence'],
#         )
#         return new_fig.get_fig()
#
#
# def relayout_data_to_range(relayout_data: dict) -> tuple[int, int]:
#     try:
#         if len(relayout_data) == 1:
#             return int(relayout_data['xaxis.range'][0]), int(relayout_data['xaxis.range'][1])
#         else:
#             result = [int(v) for v in relayout_data.values()]
#             return result[0], result[1]
#     except KeyError:
#         return tuple()
