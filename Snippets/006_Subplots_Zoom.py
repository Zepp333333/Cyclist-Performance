#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

"""
https://plotly.com/python/facet-plots/#synchronizing-axes-in-subplots-with-matches

"""
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('ride.csv')


fig = make_subplots(3, 1)
fig.add_trace(go.Scatter(x=df['time'], y=df['watts']), 1, 1)
fig.add_trace(go.Scatter(x=df['time'], y=df['distance']), 2, 1)
fig.add_trace(go.Scatter(x=df['time'], y=df['heartrate']), 3, 1)



# for i in range(1, 4):
#     fig.add_trace(go.Scatter(x=x, y=np.random.random(N)), 1, i)
fig.update_xaxes(matches='x')
fig.show()


# app.run_server(debug=True)

