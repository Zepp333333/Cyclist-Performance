#  Copyright (c) 2021. Sergei Sazonov. Some Right Reserved

'''
knowledge sources:

Drawing + Zooming:
https://dash.plotly.com/advanced-callbacks
https://www.youtube.com/watch?v=mTsZL-VmRVE
https://community.plotly.com/t/multiple-outputs-in-dash-now-available/19437

'''

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('ride.csv')

# Preparing list of figures
figures = {}
for column in df.columns[1:]:
    fig = px.line(df, x="time", y=column, width=600, height=200, template="plotly_white")
    fig.update_layout(margin=dict(l=5, r=5, t=5, b=5), xaxis_visible=False)
    figures[column] = fig

figures['watts'].add_vline(x=1000)
figures['watts'].add_vline(x=2000)

# Preparing list of graphs
graphs = []
for name, figure in figures.items():
    g = dcc.Graph(id=name, figure=figure, config={'displayModeBar': False, 'displaylogo': False})
    graphs.append(g)

# Creating app layout
app.layout = html.Div(graphs)

# Preparing list Outputs, Inputs and Stats
callback_parameters = {'outputs': [], 'inputs': [], 'states': []}
for name in figures.keys():
    out = Output(component_id=name, component_property='figure')
    inp = Input(component_id=name, component_property='relayoutData')
    st = State(component_id=name, component_property='figure')
    callback_parameters['outputs'].append(out)
    callback_parameters['inputs'].append(inp)
    callback_parameters['states'].append(st)


@app.callback(
    callback_parameters['outputs'],
    callback_parameters['inputs'],
    callback_parameters['states'],
    prevent_initial_call=True
)
def zoom_event(*args):
    outputs = []
    relayout_val = dash.callback_context.triggered[0]['value']
    l = len(args)
    for fig in args[(l // 2):]:
        try:
            fig['layout']["xaxis"]["range"] = [relayout_val['xaxis.range[0]'], relayout_val['xaxis.range[1]']]
            fig['layout']["xaxis"]["autorange"] = False
        except (KeyError, TypeError):
            fig['layout']["xaxis"]["autorange"] = True
        outputs.append(fig)

    return outputs


# @app.callback(
#     [Output(component_id='g1', component_property='figure'),
#      Output(component_id='g2', component_property='figure'),
#      Output(component_id='g3', component_property='figure')],
#     [Input(component_id='g1', component_property='relayoutData'),
#      Input(component_id='g2', component_property='relayoutData'),
#      Input(component_id='g3', component_property='relayoutData')],
#     [State(component_id='g1', component_property='figure'),
#      State(component_id='g2', component_property='figure'),
#      State(component_id='g3', component_property='figure')],
#     prevent_initial_call=True
# )
# def zoom_event(*args):
#     outputs = []
#     ctx = dash.callback_context
#     print(ctx.outputs_list, type(ctx.outputs_list))
#     value = ctx.triggered[0]['value']
#     for fig in args[3:]:
#         try:
#             fig['layout']["xaxis"]["range"] = [value['xaxis.range[0]'], value['xaxis.range[1]']]
#             fig['layout']["xaxis"]["autorange"] = False
#         except (KeyError, TypeError):
#             fig['layout']["xaxis"]["autorange"] = True
#         outputs.append(fig)
#
#     return outputs


app.run_server(debug=True)
