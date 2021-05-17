#  Copyright (c) 2021. Sergei Sazonov. Some Rights Reserved
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class CustomFigure:
    """
    Utility class holding methods simplifying creation of plotly figures
    """

    def __init__(
            self,
            chart_type: str = 'Scatter',
            data_frame: pd.DataFrame = pd.DataFrame([]),
            index_col: str = '',
            data_series: list[str] = []
    ) -> None:
        """
        Initialize instance of CustomFigure
        :param chart_type: str - type of plotly.graph_object chart
        :param data_frame: pd.DataFrame containing data to plot
        :param index_col: str - name of DataFrame column containing index (x-axis)
        :param data_series: list[str] - name of DataFrame columns to plot
        """
        self.chart_type = chart_type
        self.data_frame = data_frame
        self.index_col = index_col
        self.data_series = data_series

        self.number_of_charts = len(data_series)
        self.num_columns = 1

        self.figure = go.Figure()

    def get_fig(self) -> go.Figure:
        """
        :return: figure with required plots
        """
        if not self.check_fields_complete():
            raise ValueError(f'{self.__class__.__name__} fields incomplete')
        self.figure = make_subplots(self.number_of_charts, self.num_columns)
        for column, n in zip(self.data_series, list(range(1, self.number_of_charts + 1))):
            self.figure.add_trace(go.Scatter(
                x=self.data_frame[self.index_col],
                y=self.data_frame[column]
            ), n, 1)

        self.figure.update_xaxes(matches='x')
        return self.figure

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
