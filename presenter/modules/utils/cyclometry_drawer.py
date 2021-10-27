#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class CyclometryDrawer:
    """
    Utility class holding methods simplifying creation of set of scatter/line charts incl. rangeslider
    """

    def __init__(self, df: pd.DataFrame, index_col: str = None, series_to_plot: list[str] = None
                 ) -> None:
        """
        :param activity - activity to plot
        :param index_col: str - name of DataFrame column that contains index (x-axis)
        :param series_to_plot: list[str] - name(s) of DataFrame columns to plot in order of plotting
        """
        self.data_frame = df

        self.data_frame['time'] = pd.to_datetime(self.data_frame['secs'], unit='s')
        self.index_col = index_col
        self.series_to_plot = [series for series in series_to_plot if series in self.data_frame.columns]
        self.series_to_plot.reverse()  # reverse as plotly would render traces in reverse order
        self.intervals = []

        self.number_of_charts = len(series_to_plot)
        self.num_columns = 1

        self.figure = go.Figure()

    def get_fig(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        for chart in ['cad', 'hr', 'watts']:
            fig.add_trace(
                go.Scatter(x=self.data_frame['time'], y=self.data_frame[chart], name=chart, line={"width": 0.5}, ),
                secondary_y=False
            )

        for chart in ['awcstate', 'swcstate', 'totalWork', 'pressure']:
            fig.add_trace(
                go.Scatter(x=self.data_frame['time'], y=self.data_frame[chart], name=chart, line={"width": 0.5}),
                secondary_y=True
            )

        fig.update_layout(
            template="simple_white",
            xaxis_tickformat="%H:%M",
            )
        return fig
