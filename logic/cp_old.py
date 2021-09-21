#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd

from iobrocker import dbutil

import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = dbutil.read_dataframe_from_csv()


ftp = 290
norm_power = np.sqrt(np.sqrt(np.mean(df['watts'].rolling(30).mean() ** 4)))
intensity = norm_power / ftp
moving_time = df['time'].max()
tss = (moving_time * norm_power * intensity) / (ftp * 3600.0) * 100.0
print('\n'
      'NP: {} W \n'
      'TSS: {} \n'
      'IF: {}'.format(str(round(norm_power, 1)), str(round(tss, 1)), str(round(intensity, 2))))


# This value will be used to create a sensible log scale on the powercurve graph
logscale = 0.4

spc = pd.DataFrame(df.groupby(['watts']).time.sum())
spc.reset_index(inplace=True)
spc.sort_values(by=['watts'], ascending=False, inplace=True)

spc['work'] = spc['watts'] * spc['time']
spc['cumwork'] = spc.work.cumsum()
spc['cumdiration'] = spc['time'].cumsum()
spc['averagecumpower'] = spc['cumwork'] / spc['cumdiration']
spc['logcumdr'] = spc['cumdiration'] ** logscale

spc.reset_index(inplace=True)





fig = go.Figure()
fig.add_trace(go.Scatter(x=spc["logcumdr"], y=spc['averagecumpower']))
fig.update_xaxes(type="log")

# fig = px.scatter(spc, x="logcumdr", y="averagecumpower", log_x=True, range_x=[1, 500])
fig.show()

xticks = [1, 15, 60, 300, 600, 1200, 1800, 2700, 3600, 5400, 3600 * 2, 3600 * 3, 3600 * 4, 3600 * 5, 3600 * 6, 3600 * 8,
          3600 * 12, 3600 * 18]
