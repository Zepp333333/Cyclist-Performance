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
        if not self.check_fields_complete():
            raise ValueError(f'{self.__class__.__name__} fields incomplete')

        self.figure = go.Figure()  # redundant initialization, leave for now for transparency

        for data_stream, n in zip(self.data_series, list(range(1, self.number_of_charts + 1))):
            self.figure.add_trace(go.Scatter(
                x=self.data_frame[self.index_col],
                y=self.data_frame[data_stream],
                name=data_stream,
                yaxis=f"y{'' if n == 1 else n}"
            ))

        self.figure.update_traces(
            hoverinfo="name+x+text",
            line={"width": 0.5},
            mode="lines",
            showlegend=False
        )

        self.figure.update_layout(
            xaxis=dict(
                autorange=True,
                range=[self.data_frame.index.start, self.data_frame.index.stop],
                rangeslider=dict(
                    autorange=True,
                    range=[self.data_frame.index.start, self.data_frame.index.stop],
                ),
                type="linear"
            )
        )



        yaxis_update = dict(
            anchor="x",
            autorange=True,
            mirror=True,
            showline=True,
            side="right",
            tickfont={"color": "#673ab7"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#673ab7"},
            type="linear",
            zeroline=False
        )
        self.update_yaxis(yaxis_update)
        print(self.figure)

        self.figure.update_layout(
            dragmode="zoom",
            hovermode="x",
            # legend=dict(traceorder="reversed"),
            height=600,
            template="plotly_white",
            margin=dict(
                t=100,
                b=100
            ),
        )

        return self.figure

    def update_yaxis(self, update: dict) -> None:
        """
        Update all yaxis in self.figure.layout with provided update
          :param update: dict layout
          :return: None
        """

        # How many yaxis do we have in layout?
        yaxises = {}
        for ds, i in zip(self.data_series, range(1, len(self.data_series) + 1)):
            yaxises[ds] = f"yaxis{i}"
            if yaxises[ds] == "yaxis0":
                yaxises[ds] = "yaxis"
        num_yaxis = len(yaxises)

        # Prepare dictionary to update all yaxis
        update_dict = {}
        plot_fraction = 1 / num_yaxis

        i = 0
        for key, val in yaxises.items():
            plot_start = plot_fraction * i
            update_dict[val] = dict(update)
            update_dict[val]['range'] = [self.data_frame[key].min(), self.data_frame[key].max()]
            update_dict[val]['domain'] = [plot_start, plot_start + plot_fraction]
            i += 1
        print(update_dict)
        self.figure.update_layout(update_dict)

    # def get_fig_old(self) -> go.Figure:
    #     """
    #     :return: figure with required plots
    #     """
    #     if not self.check_fields_complete():
    #         raise ValueError(f'{self.__class__.__name__} fields incomplete')
    #
    #     # todo - replace hardcoded row_width!
    #     self.figure = make_subplots(rows=self.number_of_charts + 1, cols=self.num_columns,
    #                                 shared_xaxes=True, vertical_spacing=0.05, row_width=[0.17, 0.17, 0.17, 0.3])
    #     self.figure.update_layout(showlegend=False, template='simple_white')
    #
    #     # Create traces for each data_stream in provided data_series
    #     for data_stream, n in zip(self.data_series, list(range(2, self.number_of_charts + 2))):
    #         self.figure.add_trace(go.Scatter(
    #             x=self.data_frame[self.index_col],
    #             y=self.data_frame[data_stream]
    #         ), n, 1)
    #
    #     # add empty chart on top for interval data presentation
    #     self.figure.add_trace(go.Scatter(
    #         x=[1],
    #         y=[1],
    #         visible=False
    #     ), 1, 1)
    #
    #     # configure axis on top chart
    #     self.figure.get_subplot(1, 1).yaxis.update({'autorange': False, 'visible': False, 'fixedrange': True})
    #     self.figure.get_subplot(1, 1).xaxis.update({'visible': False})
    #
    #     # fixing y-axis on rest of the charts
    #     for subplot in range(1, self.number_of_charts + 1):
    #         self.figure.get_subplot(subplot, 1).yaxis.update({'fixedrange': True})
    #
    #     self.figure.update_layout(
    #         xaxis=dict(
    #             autorange=True,
    #             range=[self.data_frame.index.start, self.data_frame.index.stop],
    #             rangeslider=dict(
    #                 autorange=True,
    #                 range=[self.data_frame.index.start, self.data_frame.index.stop],
    #             ),
    #             # type='linear',
    #             # titlefont={"family": "Arial", "color": "#673ab7"},
    #         ),
    #     )
    #
    #     self.figure.update_layout(
    #         dragmode="zoom",
    #         hovermode="x",
    #         height=600,
    #         template="plotly_white",
    #         margin=dict(
    #             t=100,
    #             b=100
    #         ),
    #     )
    #
    #     self.draw_intervals()
    #     return self.figure

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
