#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.subplots as ps



df = pd.read_csv('ride.csv')

fig = ps.make_subplots(rows=3, cols=1)

# fig = px.line(df, x="time", y="watts",
#                  # facet_col="species",
#                  title="watts")
fig.add_trace(go.Scatter(x=df['time'], y=df["cadence"],
                 ), row=1, col=1)



# reference_line = go.Scatter(x=[2, 4],
#                             y=[4, 8],
#                             mode="lines",
#                             line=go.scatter.Line(color="gray"),
#                             showlegend=False)
#
# fig.add_trace(reference_line, row=1, col=1)
# fig.add_trace(reference_line, row=1, col=2)
# fig.add_trace(reference_line, row=1, col=3)

fig.show()
