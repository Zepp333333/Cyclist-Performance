#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import plotly.graph_objects as go

from logic import Activity


class ScatterDrawer:
    """
    Utility class holding methods simplifying creation of set of scatter/line charts incl. rangeslider
    """

    def __init__(self, activity: Activity, index_col: str = None, series_to_plot: list[str] = None
                 ) -> None:
        """
        :param activity - activity to plot
        :param index_col: str - name of DataFrame column that contains index (x-axis)
        :param series_to_plot: list[str] - name(s) of DataFrame columns to plot in order of plotting
        """
        self.data_frame = activity.dataframe
        self.data_frame['time_stamp'] = pd.to_datetime(self.data_frame['time'], unit='s')
        self.index_col = 'time_stamp'
        self.series_to_plot = [series for series in series_to_plot if series in activity.dataframe.columns]
        self.series_to_plot.reverse()  # reverse as plotly would render traces in reverse order
        self.intervals = activity.intervals

        self.number_of_charts = len(series_to_plot)
        self.num_columns = 1

        self.figure = go.Figure()

    def get_fig(self) -> go.Figure:
        """
        Produce figure containing require number of plots (self.series_to_plot) incl. rangeslider and
        boxes and annotations for existing intervals
        :return: plotly.graph_objects.Figure
        """
        if not self.check_fields_complete():
            raise ValueError(f'{self.__class__.__name__} fields incomplete')

        self.make_traces()
        self.configure_traces()
        self.configure_layouts()
        self.update_yaxis()

        self.draw_intervals()

        return self.figure

    def make_traces(self) -> None:
        """
        Produce traces for all required data streams (self.series_to_plot)
        :return: None
        """
        for data_stream, n in zip(self.series_to_plot, list(range(1, self.number_of_charts + 1))):
            self.figure.add_trace(go.Scatter(
                x=self.data_frame[self.index_col],
                y=self.data_frame[data_stream],
                name=data_stream,
                yaxis=f"y{'' if n == 1 else n}"
            ))
        # add empty trace for interval annotations on top
        self.figure.add_trace(go.Scatter(
            x=[1],
            y=[1],
            visible=False
        ))

    def configure_traces(self) -> None:
        """
        Configure traces style
        :return: None
        """
        self.figure.update_traces(
            hoverinfo="name+y+text",
            line={"width": 0.5},
            mode="lines",
            showlegend=False
        )

    def configure_layouts(self) -> None:
        """
        Configure figure layouts
        :return: None
        """
        self.figure.update_layout(
            xaxis=dict(
                autorange=True,
                rangeslider=dict(autorange=True),
                rangeselector=dict(visible=True),
            ),
            xaxis_tickformat="%H:%M",
            dragmode="zoom",
            hovermode="x",
            legend=dict(traceorder="reversed"),
            height=600,
            template="simple_white",
            margin=dict(
                t=0,
                b=100
            ),
        )

    def update_yaxis(self, update_template: dict = None) -> None:
        """
        Update all yaxis in self.figure.layout with provided optional update
        :param update_template: dict layout - optional.
                If not provided - use hardcoded below todo push out to params
        :return: None
        """
        if not update_template:
            update_template = dict(
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
        # Create list of relevant yaxis names
        yaxis = {}
        for series, i in zip(self.series_to_plot, range(1, len(self.series_to_plot) + 1)):
            yaxis[series] = f"yaxis{i}"
            # rename 'yaxis0' to 'yaxis' - as required by plotly
            if yaxis[series] == "yaxis0":
                yaxis[series] = "yaxis"
        num_yaxis = len(yaxis)

        # Produce dictionary with configuration for all yaxis
        update = {}
        plot_fraction = 1 / (num_yaxis + 1)
        i = 0
        for series, yaxis_name in yaxis.items():
            plot_start = plot_fraction * i
            update[yaxis_name] = dict(update_template)  # creating new dict to avoid mutation during iterations
            # adding range and domain params
            update[yaxis_name]['range'] = [self.data_frame[series].min(), self.data_frame[series].max()]
            update[yaxis_name]['domain'] = [plot_start, plot_start + plot_fraction]
            i += 1
        self.figure.update_layout(update)

    def refresh(self):
        return self.get_fig()

    def draw_intervals(self) -> None:
        if not self.intervals:
            return
        shapes = []
        annotations = []
        for interval in self.intervals:
            shapes.append(
                dict(fillcolor="rgba(63, 81, 181, 0.2)",
                     line={"width": 0},
                     type="rect",
                     x0=interval.start_timestamp,
                     x1=interval.end_timestamp,
                     xref="x",
                     y0=0,
                     y1=1,
                     yref="paper"
                     )
            )
            annotations.append(
                dict(
                    x=interval.start_timestamp,
                    y=1,
                    # arrowcolor="rgba(63, 81, 181, 0.2)",
                    # arrowsize=0.3,
                    # ax=0,
                    # ay=30,
                    showarrow=False,
                    text=interval.name,
                    xref="x",
                    xanchor="left",
                    yanchor="top",
                    yref="paper",
                    font=dict(
                        family="sans serif",
                        size=6,
                        color="crimson",
                    ),
                )
            )

            self.figure.update_layout(shapes=shapes, annotations=annotations)

            # self.figure.add_vrect(
            #     x0=interval.start,
            #     x1=interval.end,
            #     row="all",
            #     col="all",
            #     fillcolor="green",
            #     opacity=0.25,
            #     line_width=0,
            # editable=True,
            # edits=edits,
            # )
            # self.figure.add_annotation(
            #     x=interval.start,
            #     y=4,
            #     valign="top",
            #     xanchor="left",
            #     yanchor="top",
            #     xref="x",
            #     yref="y",
            #     text=f"{interval.name} <br>string2 <br>string3  <br>string4  <br>string5",
            #     showarrow=False)

    def check_fields_complete(self) -> bool:
        """
        :return: True if all required field of ScatterDrawer are not empty
        (None or [], or Empty Dataframe). Otherwise - False
        """
        result = self.data_frame.empty or not self.index_col or not self.series_to_plot
        return not result

    def update_data_frame(self, new_data_frame: pd.DataFrame) -> None:
        self.data_frame = new_data_frame

    def update_data_series(self, new_data_series: list[str]) -> None:
        self.series_to_plot = new_data_series
