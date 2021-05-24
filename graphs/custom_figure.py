#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from middleware import Interval, Activity


class CustomFigure:
    """
    Utility class holding methods simplifying creation of plotly figures
    """

    def __init__(
            self,
            activity: Activity,
            chart_type: str = 'Scatter',
            index_col: str = '',
            data_series: list[str] = None
    ) -> None:
        """
        Initialize instance of CustomFigure
        :param activity - activity to plot
        :param chart_type: str - type of plotly.graph_object chart
        :param index_col: str - name of DataFrame column containing index (x-axis)
        :param data_series: list[str] - name of DataFrame columns to plot
        """
        self.chart_type = chart_type
        self.data_frame = activity.df
        self.index_col = index_col
        self.data_series = data_series
        self.intervals = activity.intervals[1:]

        self.number_of_charts = len(data_series)
        self.num_columns = 1

        self.figure = go.Figure()

    def get_fig(self) -> go.Figure:
        """
        :return: figure with required plots
        """
        if not self.check_fields_complete():
            raise ValueError(f'{self.__class__.__name__} fields incomplete')

        # todo - replace hardcoded row_width!
        self.figure = make_subplots(rows=self.number_of_charts + 1, cols=self.num_columns,
                                    shared_xaxes=True, vertical_spacing=0.05, row_width=[0.17, 0.17, 0.17, 0.3])
        self.figure.update_layout(showlegend=False, template='simple_white')

        # Create traces for each data_stream in provided data_series
        for data_stream, n in zip(self.data_series, list(range(2, self.number_of_charts + 2))):
            self.figure.add_trace(go.Scatter(
                x=self.data_frame[self.index_col],
                y=self.data_frame[data_stream]
            ), n, 1)

        # add empty chart on top for interval data presentation
        self.figure.add_trace(go.Scatter(
            x=[1],
            y=[1],
            visible=False
        ), 1, 1)

        # configure axis on top chart
        self.figure.get_subplot(1, 1).yaxis.update({'autorange': False, 'visible': False, 'fixedrange': True})
        self.figure.get_subplot(1, 1).xaxis.update({'visible': False})

        # fixing y-axis on rest of the charts
        for subplot in range(1, self.number_of_charts + 1):
            self.figure.get_subplot(subplot, 1).yaxis.update({'fixedrange': True})

        self.draw_intervals()
        return self.figure

    def refresh(self):
        return self.get_fig()

    def draw_intervals(self) -> None:

        if self.intervals:
            for interval in self.intervals:
                self.figure.add_vrect(
                    x0=interval.start,
                    x1=interval.end,
                    row="all",
                    col="all",
                    fillcolor="green",
                    opacity=0.25,
                    line_width=0,
                    # editable=True,
                    # edits=edits,
                )
                self.figure.add_annotation(
                    x=interval.start,
                    y=4,
                    valign="top",
                    xanchor="left",
                    yanchor="top",
                    xref="x",
                    yref="y",
                    text=f"{interval.title} <br>string2 <br>string3  <br>string4  <br>string5",
                    showarrow=False)

    def check_fields_complete(self) -> bool:
        """
        :return: True if required field of CustomFigure are not empty
        ('' or [], or Empty Dataframe). Otherwise - False
        """
        result = self.data_frame.empty or (self.index_col == '') or (self.data_series == [])
        return not result

    def update_data_frame(self, new_data_frame: pd.DataFrame) -> None:
        self.data_frame = new_data_frame

    def update_data_series(self, new_data_series: list[str]) -> None:
        self.data_series = new_data_series

    def update_chart_type(self, new_type: str) -> None:
        self.chart_type = new_type

#
# TEST CODE

# Test CustomFigure.check_fields_complete
# df = pd.read_csv('../Snippets/ride.csv')
# f1 = CustomFigure(
#     chart_type='Scatter',
# )
# print(f1.check_fields_complete())
#
# f2 = CustomFigure(
#     chart_type='Scatter',
#     index_col='something'
# )
# print(f2.check_fields_complete())
#
# f3 = CustomFigure(
#     chart_type='Scatter',
#     index_col='something',
#     data_frame=df
# )
# print(f3.check_fields_complete())
#
# f4 = CustomFigure(
#     chart_type='Scatter',
#     index_col='something',
#     data_frame=df,
#     data_series=['something']
# )
# print(f4.check_fields_complete())


# Test CustomFigure.get_figure
# df = pd.read_csv('../Snippets/ride.csv')
# c_figure = CustomFigure(
#     chart_type='Scatter',
#     data_frame=df,
#     index_col='time',
#     data_series=['watts', 'heartrate', 'cadence']
# )
# fig = c_figure.get_fig()
# fig.show()
