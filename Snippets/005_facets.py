#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

'''
https://plotly.com/python/facet-plots/
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

# https://plotly.com/python/facet-plots/

df = px.data.stocks(indexed=True)
df2 = pd.read_csv('ride.csv')
df2 = df2.set_index('time')
df2 = df2.rename_axis('data', axis=1)
df2 = df2[0:5]

fig = px.line(df2, facet_row="data")



# fig = px.line(df, facet_col="company", facet_col_wrap=2)
# fig.add_hline(y=1, line_dash="dot", row=3, col="all",
#               annotation_text="Jan 1, 2018 baseline",
#               annotation_position="bottom right")
# fig.add_vrect(x0="2018-09-24", x1="2018-12-18", row="all", col=1,
#               annotation_text="decline", annotation_position="top left",
#               fillcolor="green", opacity=0.25, line_width=0)
fig.show()
