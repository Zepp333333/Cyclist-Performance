#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import plotly.graph_objects as go
from logic import Activity, calculate_cp


class CPPlotter:
    xticks = [1, 15, 60, 300, 600, 1200, 1800, 2700, 3600, 5400, 3600 * 2, 3600 * 3, 3600 * 4, 3600 * 5, 3600 * 6,
              3600 * 8, 3600 * 12, 3600 * 18]

    def __init__(self):
        self.xlabels = CPPlotter._ticks_to_labels(self.xticks)

    def get_cp_fig(self, activity: Activity) -> go.Figure:
        cp, metric_series_name = calculate_cp(activity)
        return self._plot_cp(cp, metric_series_name)

    def _plot_cp(self, cp: pd.DataFrame, metric_series_name: str) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cp["time"], y=cp[metric_series_name]))
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=self.xticks,
                ticktext=self.xlabels,
            ),
            template="simple_white",
            margin=dict(
                t=0,
                b=100
            ),
        )
        fig.update_xaxes(type="log")
        return fig

    @staticmethod
    def _sec_to_human_readable(seconds: int) -> str:
        h = seconds // 3600
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        return f"{str(h) + 'h' if h > 0 else ''}{str(m) + 'm' if m > 0 else ''}{str(s) + 's' if s > 0 else ''}"

    @staticmethod
    def _ticks_to_labels(ticks: list[int]) -> list[str]:
        return [CPPlotter._sec_to_human_readable(t) for t in ticks]
